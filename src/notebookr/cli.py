# notebookr.py
#!/usr/bin/env python3


import json
import subprocess
import os
import sys
import shutil
import argparse
from notebookr import __version__
from pathlib import Path
from stdlib_list import stdlib_list


def ensure_uv() -> bool:
    return shutil.which("uv") is not None


def setup_directories(notebook_path: Path) -> None:
    """Create the project directory and copy the notebook."""
    # Create project directory name from notebook name (dash-case)
    # Handle camelCase/PascalCase by adding dash before capital letters
    project_name = notebook_path.stem
    project_name = "".join(
        ["-" + c.lower() if c.isupper() else c for c in project_name]
    ).lstrip(
        "-"
    )  # change any name to dash-case
    project_name = project_name.replace(" ", "-")  # no spaces
    project_dir = Path(project_name)

    project_dir.mkdir(exist_ok=True)
    project_dir = project_dir.resolve()  # get absolute path for final message

    notebooks_dir = project_dir / "notebooks"
    # go ahead and make the notebooks directory
    notebooks_dir.mkdir(exist_ok=True)

    # copy the notebook into the notebooks directory
    shutil.copy2(notebook_path, notebooks_dir / notebook_path.name)

    return project_name, project_dir, notebooks_dir


def handle_git(project_dir: Path) -> None:
    # create .gitignore, yes we need the string like that
    gitignore_content = """
.venv/
venv/
.ipynb_checkpoints/
__pycache__/
.env
.DS_Store
*.pyc
    """.strip()

    with open(".gitignore", "w") as f:
        f.write(gitignore_content)

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])


def create_venv(venv_dir: Path) -> list[str]:
    # need to create a virtual environment
    if ensure_uv():
        print("Creating virtual environment with uv...")
        subprocess.run(["uv", "venv", str(venv_dir)], check=True)
        return ["uv", "pip"]  # uv-style pip
    else:
        print("Creating virtual environment with venv...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        pip_exe = (
            venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"
        )  # need to get the pip executable so we can install packages
        return [str(pip_exe)]


def install_requirements(pip_cmd: list[str], requirements_path: Path) -> bool:
    """Attempts to install requirements, returns True on success, False on failure."""
    try:
        # Added capture_output and text to get stderr on failure
        subprocess.run(
            pip_cmd + ["install", "-r", str(requirements_path)],
            check=True,
            capture_output=True,
            text=True        
        )
        return True
    except subprocess.CalledProcessError as e:
        print(
            "\n⚠️ Warning: Failed to install one or more packages from requirements.txt."
        )
        return False  # Failure


def setup_notebook_project(notebook_path, create_py=False):
    """Set up a development environment for a Jupyter notebook."""

    # detect python version... need a major version for stdlib_list
    detected_version = sys.version_info
    formatted_version = f"{detected_version.major}.{detected_version.minor}"

    nb_path = Path(notebook_path).resolve()  # resolve() gets absolute path
    resolved_nb_path = nb_path.resolve()
    project_name, project_dir, notebooks_dir = setup_directories(resolved_nb_path)

    os.chdir(project_dir)

    handle_git(project_dir)

    with open(notebooks_dir / nb_path.name, "r") as f:
        notebook = json.load(f)

    # get import statements from code cells
    imports = set()
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            for line in source.split("\n"):
                if line.startswith("import ") or line.startswith("from "):
                    imports.add(line.split()[1].split(".")[0])

    # create_venv() returns a list of commands to install the packages
    venv_dir = project_dir / ".venv"
    pip_commands = create_venv(venv_dir)

    # requirements.txt
    stdlib_modules = set(stdlib_list(formatted_version))
    with open("requirements.txt", "w") as f:
        f.write("ipykernel\n")  # Always include ipykernel
        ### hello reader, you could add your own packages here!
        for package in imports:
            if package not in stdlib_modules:  # Skip standard library
                f.write(f"{package}\n")

    # now we can install, regardless of whether uv is installed
    print(f"Installing requirements using: {' '.join(pip_commands)}")
    success = install_requirements(pip_commands, Path("requirements.txt"))

    if create_py:
        print("Converting notebook to Python...")
        subprocess.run(["jupyter", "nbconvert", "--to", "python", nb_path.name])

    if success:
        print("\n✨ Project setup complete! ✨")
        print(f"\nYour notebook environment is ready at: {project_dir}")
        print(f"Activate it with: cd {project_dir} && source .venv/bin/activate")
    else:
        print("\n⚠️ Project setup generated, but package installation failed.")
        print("   Please review the warnings above and check 'requirements.txt'.")
        print("   You may need to activate the environment and install manually:")
        print(f"   cd {project_dir}")
        print("   source .venv/bin/activate")
        print(f"   {' '.join(pip_commands)} install -r requirements.txt")


def main():
    parser = argparse.ArgumentParser(
        description="Set up a development environment for a Jupyter notebook. Works best with uv installed."
    )
    parser.add_argument("notebook", help="Path to the notebook file")
    parser.add_argument(
        "--with_py",
        action="store_true",
        help="Also create a Python file from the notebook using nbconvert",
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()

    setup_notebook_project(args.notebook, create_py=args.with_py)

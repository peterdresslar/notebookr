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

def ensure_uv() -> bool:
    return shutil.which("uv") is not None

def setup_directories(notebook_path: Path) -> None:
    """Create the project directory and copy the notebook."""
    # Create project directory name from notebook name (dash-case)
    # Handle camelCase/PascalCase by adding dash before capital letters
    project_name = notebook_path.stem
    project_name = ''.join(['-'+c.lower() if c.isupper() else c for c in project_name]).lstrip('-')  # change any name to dash-case
    project_name = project_name.replace(' ', '-') # no spaces
    project_dir = Path(project_name)
    
    project_dir.mkdir(exist_ok=True)
    project_dir = project_dir.resolve()  # get absolute path for final message

    notebooks_dir = project_dir / 'notebooks'
    # go ahead and make the notebooks directory
    notebooks_dir.mkdir(exist_ok=True)
    
    # copy the notebook into the notebooks directory
    shutil.copy2(notebook_path, notebooks_dir / notebook_path.name)
    
    return project_name, project_dir, notebooks_dir

def create_venv(venv_dir: Path) -> list[str]:
    # need to create a virtual environment
    if ensure_uv():
        subprocess.run(["uv", "venv", str(venv_dir)], check=True)
        return ["uv", "pip"]                              # uv-style pip
    else:
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        pip_exe = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"   # need to get the pip executable so we can install packages
        return [str(pip_exe)]
    
def install_requirements(pip_cmd: list[str], requirements_path: Path) -> None:
    subprocess.run(pip_cmd + ["install", "-r", str(requirements_path)], check=True)

def setup_notebook_project(notebook_path, create_py=False):
    """Set up a development environment for a Jupyter notebook."""
    
    has_uv = ensure_uv()

    nb_path = Path(notebook_path).resolve()  # resolve() gets absolute path
    resolved_nb_path = nb_path.resolve()
    project_name, project_dir, notebooks_dir = setup_directories(resolved_nb_path)
    
    os.chdir(project_dir)
    
    with open(notebooks_dir / nb_path.name, 'r') as f:
        notebook = json.load(f)
    
    # get import statements from code cells
    imports = set()
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            for line in source.split('\n'):
                if line.startswith('import ') or line.startswith('from '):
                    imports.add(line.split()[1].split('.')[0])
    
    # if uv is not installed note to the user that we are skipping the step
    if not has_uv:
        print("Note: uv is not installed, skipping the step to create a virtual environment.")
    else:
        create_venv(project_dir / '.venv')
    
    #requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write('ipykernel\n')  # Always include ipykernel
        ### hello reader, you could add your own packages here!
        for package in imports:
            if package not in ['os', 'sys', 'math']:  # Skip standard library
                f.write(f'{package}\n')
    
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
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
    
    if has_uv:
        subprocess.run(['uv', 'pip', 'install', '-r', 'requirements.txt'])
    else:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    if create_py:
        print("Converting notebook to Python...")
        subprocess.run(['jupyter', 'nbconvert', '--to', 'python', nb_path.name])
    
    print(f"\n✨ Project setup complete! ✨") # noqa ... come on ruff thereʻre sparkles
    print(f"\nYour notebook environment is ready at: {project_dir}")
    
def main():
    parser = argparse.ArgumentParser(description='Set up a development environment for a Jupyter notebook.')
    parser.add_argument('notebook', help='Path to the notebook file')
    parser.add_argument('--with_py', action='store_true', help='Also create a Python file from the notebook using nbconvert')
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    
    setup_notebook_project(args.notebook, create_py=args.with_py)
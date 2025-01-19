#!/usr/bin/env python3
import json
import subprocess
import os
import sys
from pathlib import Path

def ensure_uv():
    """Ensure UV is installed"""
    try:
        subprocess.run(['uv', '--version'], capture_output=True)
    except FileNotFoundError:
        print("Installing UV...")
        subprocess.run(['pip', 'install', 'uv'])

def setup_notebook_project(notebook_path):
    """Set up a development environment for a Jupyter notebook."""
    
    ensure_uv()

    # Convert notebook path to Path object
    nb_path = Path(notebook_path).resolve()  # resolve() gets absolute path
    
    # Create project directory name from notebook name (dash-case)
    project_name = nb_path.stem.lower().replace(' ', '-')
    project_dir = Path(project_name)
    
    # Create project directory
    project_dir.mkdir(exist_ok=True)
    project_dir = project_dir.resolve()  # get absolute path for final message
    
    # Copy notebook to project directory
    import shutil
    shutil.copy2(notebook_path, project_dir / nb_path.name)
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Rest of your existing code here, starting with reading the notebook
    with open(nb_path.name, 'r') as f:
        notebook = json.load(f)
    
    # Extract import statements from code cells
    imports = set()
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            for line in source.split('\n'):
                if line.startswith('import ') or line.startswith('from '):
                    imports.add(line.split()[1].split('.')[0])
    
    # Create virtual environment using UV
    subprocess.run(['uv', 'venv'])
    
    # Create requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write('jupyter\n')  # Always include jupyter
        f.write('ipywidgets\n')  # Always include ipywidgets. 
        ### hello reader, you could add your own packages here!
        for package in imports:
            if package not in ['os', 'sys', 'math']:  # Skip standard library
                f.write(f'{package}\n')
    
    # Create .gitignore
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
    
    # Initialize git repo if not already initialized
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
    
    # Install requirements using UV
    subprocess.run(['uv', 'pip', 'install', '-r', 'requirements.txt'])
    
    # Final success message
    print(f"\n✨ Project setup complete! ✨") # noqa ... come on ruff thereʻs sparkles
    print(f"\nYour notebook environment is ready at: {project_dir}")
    print("\nNext steps:")
    print(f"  cd {project_name}")
    print("  code .  # If using VSCode")
    print("  # or open with your preferred editor\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: notebookr path/to/notebook.ipynb")
        sys.exit(1)
    
    setup_notebook_project(sys.argv[1])
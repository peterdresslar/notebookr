#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import argparse
from pathlib import Path

def ensure_uv():
    """Ensure UV is installed"""
    try:
        subprocess.run(['uv', '--version'], capture_output=True)
    except FileNotFoundError:
        print("Installing UV...")
        subprocess.run(['pip', 'install', 'uv'])

def setup_notebook_project(notebook_path, create_py=False):
    """Set up a development environment for a Jupyter notebook."""
    
    ensure_uv()

    # Convert notebook path to Path object
    nb_path = Path(notebook_path).resolve()  # resolve() gets absolute path
    
    # Create project directory name from notebook name (dash-case)
    # Handle camelCase/PascalCase by adding dash before capital letters
    project_name = nb_path.stem
    project_name = ''.join(['-'+c.lower() if c.isupper() else c for c in project_name]).lstrip('-')
    project_name = project_name.replace(' ', '-')
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
    
    # After copying the notebook, convert to Python if requested
    if create_py:
        print("Converting notebook to Python...")
        subprocess.run(['jupyter', 'nbconvert', '--to', 'python', nb_path.name])
    
    # Final success message
    print(f"\n✨ Project setup complete! ✨") # noqa ... come on ruff thereʻs sparkles
    print(f"\nYour notebook environment is ready at: {project_dir}")
    print("\nNext steps:")
    print(f"  cd {project_name}")
    print("  code .  # If using VSCode")
    print("  # or open with your preferred editor\n")

def main():
    parser = argparse.ArgumentParser(description='Set up a development environment for a Jupyter notebook.')
    parser.add_argument('notebook', help='Path to the notebook file')
    parser.add_argument('--with_py', action='store_true', help='Also create a Python file from the notebook using nbconvert')
    args = parser.parse_args()
    
    setup_notebook_project(args.notebook, create_py=args.with_py)
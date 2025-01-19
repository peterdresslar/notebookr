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
    
    # Read the notebook to extract imports
    with open(notebook_path, 'r') as f:
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

def main():
    if len(sys.argv) != 2:
        print("Usage: notebookr path/to/notebook.ipynb")
        sys.exit(1)
    
    setup_notebook_project(sys.argv[1])
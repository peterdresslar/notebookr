# notebook-setup

A simple tool to set up development environments for Jupyter notebooks.

## Installation

```bash

pip install notebookr

`

## Usage

```bash

notebookr path/to/your/notebook.ipynb

`

This will:
1. Create a virtual environment
2. Generate requirements.txt based on imports in your notebook
3. Create a .gitignore
4. Initialize a git repository
5. Install required packages
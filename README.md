# notebookr

[![PyPI version](https://badge.fury.io/py/notebookr.svg)](https://badge.fury.io/py/notebookr)
[![Python](https://img.shields.io/pypi/pyversions/notebookr.svg)](https://pypi.org/project/notebookr/)
[![Downloads](https://static.pepy.tech/badge/notebookr)](https://pepy.tech/project/notebookr)

A simple tool to set up development environments for Jupyter notebooks. My motivation: people frequently email or file-share Jupyter notebooks, which generally short-circuits my normal flow for receiving, working with, and managing code (usually via GitHub). So, whatʻs the fastest, easiest way to get these loose notebooks into flow?

Using notebookr you can typically cut the setup process down to a very short workflow:

1. Receive and save Python notebook (.ipynb) file into a working directory
2. Open a terminal
3. `notebookr SomeNotebook.ipynb`

The package runs and creates a project folder with your notebook. At this point, if you are using an IDE, you might:

4. `code some-notebook`
5. `source .venv/bin/activate` 
... or:
6. `.venv\Scripts\activate` # windows

- or - if you are using Jupyter

4. `jupyter lab --notebook-dir=some-notebook`

Notebookr will give you
- A git-initialized, uv-initialized project folder with a name based on the notebook name
- The uv virtual environment at `.venv/`, ready to be activated.
- A simple .gitignore with common patterns, including especially that .venv pattern
- A `pyproject.toml` or `requirements.txt` (optional) file with dependencies read in from the notebook.
- A `notebooks/` folder with your notebook safely tucked away.

# Installation

```bash
pip install notebookr
```
# or
```bash
uv add notebookr
```

# Usage

```bash
notebookr path/to/your/notebook.ipynb
```

```bash
notebookr --with_py path/to/your/notebook.ipynb # Also creates a python copy of the notebook
```

This will:
1. Create a virtual environment
2. Generate requirements.txt based on imports in your notebook
3. Create a .gitignore
4. Initialize a git repository
5. Install required packages

# Version
0.1.1 added `--with_py`
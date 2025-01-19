# notebookr

[![PyPI version](https://badge.fury.io/py/notebookr.svg)](https://badge.fury.io/py/notebookr)
[![Python](https://img.shields.io/pypi/pyversions/notebookr.svg)](https://pypi.org/project/notebookr/)
[![Downloads](https://static.pepy.tech/badge/notebookr)](https://pepy.tech/project/notebookr)

A simple tool to set up development environments for Jupyter notebooks. My motivation: basically, Jupyter notebooks are about the only program type for which it is *still* generally practiced to distribute the code through email or file sharing. 

I was tired of running the same setup process over and over with notebooks that are usually emailed to me. I work in IDEs, usually Cursor and sometimes VSCode, and naturally also work with git.

I complained to claude-3.5-sonnet about that, and here we are. 

> Claude: "three times in this chat you complained, but whoʻs counting? I thought it would be faster to write the library."

Using notebookr you can typically cut that setup process down to a very short workflow:

1. Receive and save python notebook (.ipynb) file into a working directory
2. Open a terminal
3. `notebookr SomeNotebookYouGot.ipynb`
4. `code some-notebook-you-got`

Once your code editor opens, depening on your workflow, youʻll probably want to open the terminal (ctrl-`) and enter either

5. `source .venv/bin/activate` 
#     * OR *
5w. `.venv\Scripts\activate` # windows

## Installation

```bash
pip install notebookr
```
# or
```bash
uv add notebookr
```

## Usage

```bash
notebookr path/to/your/notebook.ipynb
```

This will:
1. Create a virtual environment
2. Generate requirements.txt based on imports in your notebook
3. Create a .gitignore
4. Initialize a git repository
5. Install required packages
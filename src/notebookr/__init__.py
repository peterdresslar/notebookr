"""Setup development environments for Jupyter notebooks using UV."""

__version__ = "0.1.5"

from .cli import setup_notebook_project

__all__ = ["setup_notebook_project"]
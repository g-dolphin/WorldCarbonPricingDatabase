
# Configuration file for the Sphinx documentation builder.

import os
import sys
from datetime import datetime

# Add the project root to sys.path so autodoc can find the code
sys.path.insert(0, os.path.abspath(".."))

project = "World Carbon Pricing Database"
author = "Geoffroy Dolphin"
copyright = f"{datetime.now().year}, {author}"
release = "0.1"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

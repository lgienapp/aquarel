import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'aquarel'
copyright = '2024, Lukas Gienapp'
author = 'Lukas Gienapp'
release = '0.0.6'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ 'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo', 'sphinx.ext.mathjax',
               'sphinx.ext.ifconfig', 'sphinx.ext.viewcode', 'sphinx.ext.githubpages', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

autodoc_typehints = "description"
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Defyes"
copyright = "2024, Karpatkey"
author = "Karpatkey"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
]

autoclass_content = "class"
autodoc_member_order = "bysource"
add_module_names = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
html_theme_options = {
    "description": "Defyes is a Python library for retrieving data from DeFi protocols.",
    "page_width": "1200px",
    "extra_nav_links": {
        "Source code": "https://github.com/KarpatkeyDAO/defyes/",
        "Issue tracker": "https://github.com/KarpatkeyDAO/defyes/issues",
        "Karpatkey": "https://www.karpatkey.com/",
    },
}

autodoc_default_options = {
    "member-order": "bysource",
}

import os
import sys

sys.path.insert(0, os.path.abspath('../../../'))



project = 'Proyecto Vivero'
copyright = '2025, IGNACIO ALCANIZ'
author = 'IGNACIO ALCANIZ'
release = '1.0.0'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',  
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


language = 'es'


html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']



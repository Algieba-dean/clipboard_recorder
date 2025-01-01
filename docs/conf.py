import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Clipboard Recorder'
copyright = '2024'
author = 'Algieba'

# 扩展配置
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

# 模板配置
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML输出配置
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'Clipboard Recorder Documentation'
html_short_title = 'Clipboard Recorder'
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# 国际化配置
language = 'zh_CN'
locale_dirs = ['locale/']
gettext_compact = False

# autodoc配置
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# napoleon配置
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None 
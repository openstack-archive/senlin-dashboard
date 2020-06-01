# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

sys.path.insert(0, ROOT)

# This is required for ReadTheDocs.org, but isn't a bad idea anyway.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'senlin_dashboard.test.settings')
django.setup()

# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*')
# or your custom ones.
extensions = ['sphinx.ext.todo',
              'sphinx.ext.coverage',
              'sphinx.ext.viewcode',
              'sphinxcontrib.apidoc',
              'openstackdocstheme',
              ]

# Autodoc generation is a bit aggressive and a nuisance when doing heavy
# text edit cycles.
# execute "export SPHINX_DEBUG=1" in your terminal to disable

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'senlin-dashboard'
copyright = u'2015, OpenStack Foundation'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['**/#*', '**~', '**/#*#']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# sphinxcontrib-apidoc
apidoc_module_dir = '../../senlin_dashboard'
apidoc_output_dir = 'contributor/api'
apidoc_excluded_paths = [
    'test',
]

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages. Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_static_path = []
html_theme = 'openstackdocs'

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

# -- Options for openstackdocstheme -------------------------------------------
openstackdocs_repo_name = 'openstack/senlin-dashboard'
openstackdocs_auto_name = False
openstackdocs_bug_project = 'senlin-dashboard'
openstackdocs_bug_tag = ''

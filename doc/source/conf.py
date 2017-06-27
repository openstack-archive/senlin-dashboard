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
import subprocess
import sys
import warnings

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
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

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages. Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_static_path = []
html_theme = 'openstackdocs'

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'
git_cmd = ["git", "log", "--pretty=format:'%ad, commit %h'", "--date=local",
           "-n1"]
try:
    html_last_updated_fmt = subprocess.check_output(git_cmd).decode('utf-8')
except Exception:
    warnings.warn('Cannot get last updated time from git repository. '
                  'Not setting "html_last_updated_fmt".')

# -- Options for openstackdocstheme -------------------------------------------
repository_name = 'openstack/senlin-dashboard'
bug_project = 'senlin-dashboard'
bug_tag = ''

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.nodes.tables import NodesTable


class IndexView(tables.DataTableView):
    table_class = NodesTable
    template_name = 'cluster/nodes/index.html'

    def get_data(self):
        try:
            nodes = senlin.node_list(self.request)
        except Exception:
            nodes = []
            exceptions.handle(self.request,
                              _('Unable to retrieve nodes.'))
        return nodes

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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon.utils import memoized

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.nodes import forms as nodes_forms
from senlin_dashboard.cluster.nodes.tables import NodesTable
from senlin_dashboard.cluster.nodes import tabs as nodes_tabs


class IndexView(tables.DataTableView):
    table_class = NodesTable
    template_name = 'cluster/nodes/index.html'
    page_title = _("Nodes")

    def get_data(self):
        try:
            params = {}
            nodes = senlin.node_list(self.request, params)
        except Exception:
            nodes = []
            exceptions.handle(self.request,
                              _('Unable to retrieve nodes.'))
        return nodes


class CreateView(forms.ModalFormView):
    template_name = 'cluster/nodes/create.html'
    page_title = _("Create Node")
    form_class = nodes_forms.CreateForm
    submit_url = reverse_lazy("horizon:cluster:nodes:create")
    success_url = reverse_lazy("horizon:cluster:nodes:index")


class DetailView(tabs.TabView):
    tab_group_class = nodes_tabs.NodeDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ node.name }}"
    profile_url = 'horizon:cluster:profiles:detail'

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get initial node information
            node_id = self.kwargs["node_id"]
            node = senlin.node_get(self.request, node_id)
        except Exception:
            msg = _("Unable to retrieve node.")
            url = reverse_lazy("horizon:cluster:nodes:index")
            exceptions.handle(self.request, msg, redirect=url)
        return node

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        table = NodesTable(self.request)
        node = self.get_object()
        node.profile_url = reverse_lazy(self.profile_url,
                                        args=[node.profile_id])
        context["actions"] = table.render_row_actions(node)
        context["node"] = node
        context["url"] = reverse_lazy("horizon:cluster:nodes:index")
        return context

    def get_tabs(self, request, *args, **kwargs):
        node = self.get_object()
        return self.tab_group_class(request, node=node, **kwargs)

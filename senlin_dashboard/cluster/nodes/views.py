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

import yaml

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

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        filters = self.get_filters()

        prev_marker = self.request.GET.get(
            NodesTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                NodesTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        try:
            nodes, self._more, self._prev = senlin.node_list(
                self.request,
                marker=marker,
                paginate=True,
                reversed_order=reversed_order,
                filters=filters)
        except Exception:
            self._prev = self._more = False
            nodes = []
            msg = _('Unable to retrieve nodes.')
            exceptions.handle(self.request, msg)
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
    cluster_url = 'horizon:cluster:clusters:detail'

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
        if node.cluster_id:
            node.cluster_url = reverse_lazy(self.cluster_url,
                                            args=[node.cluster_id])
        context["actions"] = table.render_row_actions(node)
        context["node"] = node
        context["url"] = reverse_lazy("horizon:cluster:nodes:index")
        return context

    def get_tabs(self, request, *args, **kwargs):
        node = self.get_object()
        return self.tab_group_class(request, node=node, **kwargs)


class UpdateView(forms.ModalFormView):
    template_name = 'cluster/nodes/update.html'
    page_title = _("Update Node")
    form_class = nodes_forms.UpdateNodeForm
    submit_url = reverse_lazy("horizon:cluster:nodes:update")
    success_url = reverse_lazy("horizon:cluster:nodes:index")

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get initial node information
            node_id = self.kwargs["node_id"]
            node = senlin.node_get(self.request, node_id)
            # Metadata in update form should be empty rather than {}
            if not node.metadata:
                metadata = None
            else:
                metadata = yaml.safe_dump(
                    node.metadata,
                    default_flow_style=False)
            node_dict = {"node_id": node_id,
                         "name": node.name,
                         "profile_id": node.profile_id,
                         "role": node.role,
                         "metadata": metadata}

        except Exception:
            msg = _("Unable to retrieve node.")
            url = reverse_lazy("horizon:cluster:nodes:index")
            exceptions.handle(self.request, msg, redirect=url)
        return node_dict

    def get_context_data(self, **kwargs):
        args = (self.kwargs["node_id"],)
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["node"] = self.get_object()
        context["submit_url"] = reverse_lazy(
            "horizon:cluster:nodes:update",
            args=args)
        return context

    def get_initial(self):
        return self.get_object()

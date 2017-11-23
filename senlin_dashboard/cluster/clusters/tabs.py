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
from horizon import tabs

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.nodes import event_tables
from senlin_dashboard.cluster.nodes import tables as node_table
from senlin_dashboard.cluster.nodes import tabs as node_tab


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("cluster/clusters/_detail_overview.html")

    def get_context_data(self, request):
        return {"cluster": self.tab_group.kwargs['cluster']}


class EventTab(node_tab.EventTab):

    def get_event_data(self):

        prev_marker = self.request.GET.get(
            event_tables.EventsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                event_tables.EventsTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None

        cluster_id = self.tab_group.kwargs['cluster_id']
        try:
            filters = {"obj_id": cluster_id}
            events, self._more, self._prev = senlin.event_list(
                self.request,
                marker=marker,
                paginate=True,
                reversed_order=reversed_order,
                filters=filters)
        except Exception:
            self._prev = self._more = False
            events = []
            exceptions.handle(self.request,
                              _('Unable to retrieve node event list.'))
        return events


class NodesTab(tabs.TableTab):
    name = _("Nodes")
    slug = "nodes"
    table_classes = (node_table.NodesTable,)
    template_name = "cluster/clusters/_detail_nodes.html"
    preload = False

    def get_nodes_data(self):
        cluster_id = self.tab_group.kwargs['cluster_id']
        try:
            cluster_nodes, self._more, self._prev = senlin.node_list(
                self.request,
                cluster_id=cluster_id)
        except Exception:
            cluster_nodes = []
            exceptions.handle(self.request,
                              _('Unable to retrieve nodes from cluster.'))
        return cluster_nodes


class ClusterDetailTabs(tabs.TabGroup):
    slug = "cluster_details"
    sticky = True
    tabs = (OverviewTab, EventTab, NodesTab)

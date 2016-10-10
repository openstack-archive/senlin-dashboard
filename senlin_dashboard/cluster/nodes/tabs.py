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


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("cluster/nodes/_detail_overview.html")

    def get_context_data(self, request):
        return {"node": self.tab_group.kwargs['node']}


class EventTab(tabs.TableTab):
    name = _("Event")
    slug = "event"
    table_classes = (event_tables.EventsTable,)
    template_name = "cluster/nodes/_detail_event.html"
    preload = False

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_event_data(self):

        prev_marker = self.request.GET.get(
            event_tables.EventsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                event_tables.EventsTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None

        node_id = self.tab_group.kwargs['node_id']
        try:
            filters = {"obj_id": node_id}
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


class NodeDetailTabs(tabs.TabGroup):
    slug = "node_details"
    sticky = True
    tabs = (OverviewTab, EventTab)

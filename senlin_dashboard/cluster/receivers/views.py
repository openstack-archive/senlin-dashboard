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
from senlin_dashboard.cluster.receivers import forms as receivers_forms
from senlin_dashboard.cluster.receivers.tables import ReceiversTable
from senlin_dashboard.cluster.receivers import tabs as receivers_tabs


class IndexView(tables.DataTableView):
    table_class = ReceiversTable
    template_name = 'cluster/receivers/index.html'
    page_title = _("Receivers")

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        filters = self.get_filters()

        prev_marker = self.request.GET.get(
            ReceiversTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                ReceiversTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        try:
            receivers, self._more, self._prev = senlin.receiver_list(
                self.request,
                marker=marker,
                paginate=True,
                reversed_order=reversed_order,
                filters=filters)
        except Exception:
            self._prev = self._more = False
            receivers = []
            msg = _('Unable to retrieve receivers.')
            exceptions.handle(self.request, msg)
        return receivers


class CreateView(forms.ModalFormView):
    template_name = 'cluster/receivers/create.html'
    page_title = _("Create Receiver")
    form_class = receivers_forms.CreateReceiverForm
    submit_url = reverse_lazy("horizon:cluster:receivers:create")
    success_url = reverse_lazy("horizon:cluster:receivers:index")


class DetailView(tabs.TabView):
    tab_group_class = receivers_tabs.ReceiverDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ receiver.name }}"

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get initial receiver information
            receiver_id = self.kwargs["receiver_id"]
            receiver = senlin.receiver_get(self.request, receiver_id)
        except Exception:
            msg = _("Unable to retrieve receiver.")
            url = reverse_lazy("horizon:cluster:receivers:index")
            exceptions.handle(self.request, msg, redirect=url)
        return receiver

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        table = ReceiversTable(self.request)
        receiver = self.get_object()
        context["actions"] = table.render_row_actions(receiver)
        context["receiver"] = receiver
        context["url"] = reverse_lazy("horizon:cluster:receivers:index")
        return context

    def get_tabs(self, request, *args, **kwargs):
        receiver = self.get_object()
        return self.tab_group_class(request, receiver=receiver, **kwargs)

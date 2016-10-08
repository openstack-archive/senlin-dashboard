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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.clusters import forms as clusters_forms
from senlin_dashboard.cluster.clusters.tables import AttachedPoliciesTable
from senlin_dashboard.cluster.clusters.tables import ClustersTable
from senlin_dashboard.cluster.clusters import tabs as clusters_tabs

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon.utils import memoized


class IndexView(tables.DataTableView):
    table_class = ClustersTable
    template_name = 'cluster/clusters/index.html'
    page_title = _("Clusters")

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        filters = self.get_filters()

        prev_marker = self.request.GET.get(
            ClustersTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                ClustersTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        try:
            clusters, self._more, self._prev = senlin.cluster_list(
                self.request,
                marker=marker,
                paginate=True,
                reversed_order=reversed_order,
                filters=filters)
        except Exception:
            self._prev = self._more = False
            clusters = []
            msg = _('Unable to retrieve clusters.')
            exceptions.handle(self.request, msg)
        return clusters


class CreateView(forms.ModalFormView):
    template_name = 'cluster/clusters/create.html'
    page_title = _("Create Cluster")
    form_class = clusters_forms.CreateForm
    submit_url = reverse_lazy("horizon:cluster:clusters:create")
    success_url = reverse_lazy(clusters_forms.INDEX_URL)


class DetailView(tabs.TabView):
    tab_group_class = clusters_tabs.ClusterDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ cluster.name }}"
    profile_url = 'horizon:cluster:profiles:detail'

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get cluster information
            cluster_id = self.kwargs["cluster_id"]
            cluster = senlin.cluster_get(self.request, cluster_id)
            cluster.profile_url = reverse_lazy(self.profile_url,
                                               args=[cluster.profile_id])
        except Exception:
            msg = _("Unable to retrieve cluster.")
            url = reverse_lazy(clusters_forms.INDEX_URL)
            exceptions.handle(self.request, msg, redirect=url)
        return cluster

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        table = ClustersTable(self.request)
        cluster = self.get_object()
        policies = senlin.cluster_policy_list(
            self.request, self.kwargs['cluster_id'], {})
        cluster.policies = policies
        context["actions"] = table.render_row_actions(cluster)
        context["cluster"] = cluster
        return context

    def get_tabs(self, request, *args, **kwargs):
        cluster = self.get_object()
        return self.tab_group_class(request, cluster=cluster, **kwargs)


class ManagePoliciesView(tables.DataTableView, forms.ModalFormView):
    table_class = AttachedPoliciesTable
    form_class = clusters_forms.ManagePoliciesForm
    form_id = "manage_policies"
    modal_header = _("Manage Policies")
    modal_id = "manage_policies"
    template_name = 'cluster/clusters/manage_policies.html'
    submit_url = "horizon:cluster:clusters:manage_policies"
    success_url = reverse_lazy("horizon:cluster:clusters:index")
    page_title = _("Manage Policies")

    def get_data(self):
        policies = senlin.cluster_policy_list(
            self.request, self.kwargs['cluster_id'], {})
        return policies

    def get_context_data(self, **kwargs):
        context = super(ManagePoliciesView, self).get_context_data(**kwargs)
        args = (self.kwargs['cluster_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        context['form'] = self.get_form()
        return context

    def get_initial(self):
        return {'cluster_id': self.kwargs['cluster_id']}

    def get(self, request, *args, **kwargs):
        # Table action handling
        handled = self.construct_tables()
        if handled:
            return handled
        return self.render_to_response(self.get_context_data(**kwargs))

    @memoized.memoized_method
    def get_form(self, **kwargs):
        form_class = kwargs.get('form_class', self.get_form_class())
        return super(ManagePoliciesView, self).get_form(form_class)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.get(request, *args, **kwargs)

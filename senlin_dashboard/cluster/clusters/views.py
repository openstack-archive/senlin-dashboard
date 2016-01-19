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

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.clusters import forms as clusters_forms
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

    def get_data(self):
        try:
            params = {}
            clusters = senlin.cluster_list(self.request, params)
        except Exception:
            clusters = []
            exceptions.handle(self.request,
                              _('Unable to retrieve clusters.'))
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
        context["actions"] = table.render_row_actions(cluster)
        context["cluster"] = cluster
        context["url"] = reverse_lazy(clusters_forms.INDEX_URL)
        return context

    def get_tabs(self, request, *args, **kwargs):
        cluster = self.get_object()
        return self.tab_group_class(request, cluster=cluster, **kwargs)

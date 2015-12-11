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

from horizon import exceptions
from horizon import forms
from horizon import tables


class IndexView(tables.DataTableView):
    table_class = ClustersTable
    template_name = 'cluster/clusters/index.html'
    page_title = _("Clusters")

    def get_data(self):
        try:
            clusters = senlin.cluster_list(self.request)
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
    success_url = reverse_lazy("horizon:cluster:clusters:index")

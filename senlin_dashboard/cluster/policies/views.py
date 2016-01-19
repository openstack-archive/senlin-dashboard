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

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.policies import forms as policies_forms
from senlin_dashboard.cluster.policies.tables import PoliciesTable
from senlin_dashboard.cluster.policies import tabs as policies_tabs

from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
from horizon.utils import memoized


class IndexView(tables.DataTableView):
    table_class = PoliciesTable
    template_name = 'cluster/policies/index.html'
    page_title = _("Policies")

    def get_data(self):
        try:
            params = {}
            policies = senlin.policy_list(self.request, params)
        except Exception:
            policies = []
            exceptions.handle(self.request,
                              _('Unable to retrieve policies.'))
        return policies


class CreateView(forms.ModalFormView):
    template_name = 'cluster/policies/create.html'
    page_title = _("Create Policy")
    form_class = policies_forms.CreatePolicyForm
    submit_url = reverse_lazy(policies_forms.CREATE_URL)
    success_url = reverse_lazy(policies_forms.INDEX_URL)


class DetailView(tabs.TabView):
    tab_group_class = policies_tabs.PolicyDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ policy.name }}"

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get policy information
            policy_id = self.kwargs["policy_id"]
            policy = senlin.policy_get(self.request, policy_id)
            policy.policy_spec = yaml.safe_dump(policy.spec,
                                                default_flow_style=False)
        except Exception:
            msg = _("Unable to retrieve policy.")
            url = reverse_lazy(policies_forms.INDEX_URL)
            exceptions.handle(self.request, msg, redirect=url)
        return policy

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        table = PoliciesTable(self.request)
        policy = self.get_object()
        context["actions"] = table.render_row_actions(policy)
        context["policy"] = policy
        context["url"] = reverse_lazy(policies_forms.INDEX_URL)
        return context

    def get_tabs(self, request, *args, **kwargs):
        policy = self.get_object()
        return self.tab_group_class(request, policy=policy, **kwargs)

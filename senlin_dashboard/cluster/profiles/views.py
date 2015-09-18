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

from horizon import forms
from horizon import tables

from senlin_dashboard.api import senlin
from senlin_dashboard.cluster.profiles import forms as profiles_forms
from senlin_dashboard.cluster.profiles.tables import ProfilesTable


class IndexView(tables.DataTableView):
    table_class = ProfilesTable
    template_name = 'cluster/profiles/index.html'

    def get_data(self):
        return senlin.profile_list(self.request)


class CreateView(forms.ModalFormView):
    template_name = 'cluster/profiles/create.html'
    page_title = _("Create Profile")
    form_class = profiles_forms.CreateProfileForm
    submit_url = reverse_lazy(profiles_forms.CREATE_URL)
    success_url = reverse_lazy(profiles_forms.INDEX_URL)

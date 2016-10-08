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
from senlin_dashboard.cluster.profiles import forms as profiles_forms
from senlin_dashboard.cluster.profiles.tables import ProfilesTable
from senlin_dashboard.cluster.profiles import tabs as profiles_tabs

import yaml


class IndexView(tables.DataTableView):
    table_class = ProfilesTable
    template_name = 'cluster/profiles/index.html'
    page_title = _("Profiles")

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def get_data(self):
        filters = self.get_filters()

        prev_marker = self.request.GET.get(
            ProfilesTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                ProfilesTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        try:
            profiles, self._more, self._prev = senlin.profile_list(
                self.request,
                marker=marker,
                paginate=True,
                reversed_order=reversed_order,
                filters=filters)
        except Exception:
            self._prev = self._more = False
            profiles = []
            msg = _('Unable to retrieve profiles.')
            exceptions.handle(self.request, msg)
        return profiles


class CreateView(forms.ModalFormView):
    template_name = 'cluster/profiles/create.html'
    page_title = _("Create Profile")
    form_class = profiles_forms.CreateProfileForm
    submit_url = reverse_lazy(profiles_forms.CREATE_URL)
    success_url = reverse_lazy(profiles_forms.INDEX_URL)


class UpdateView(forms.ModalFormView):
    template_name = 'cluster/profiles/update.html'
    page_title = _("Update Profile")
    form_class = profiles_forms.UpdateProfileForm
    submit_url = reverse_lazy(profiles_forms.UPDATE_URL)
    success_url = reverse_lazy(profiles_forms.INDEX_URL)

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get initial profile information
            profile_id = self.kwargs["profile_id"]
            profile = senlin.profile_get(self.request, profile_id)
            # Metadata in update form should be empty rather than {}
            if not profile.metadata:
                metadata = None
            else:
                metadata = yaml.safe_dump(
                    profile.metadata,
                    default_flow_style=False)
            profile_dict = {"profile_id": profile_id,
                            "name": profile.name,
                            "type": profile.type,
                            "spec": yaml.safe_dump(
                                profile.spec,
                                default_flow_style=False),
                            "metadata": metadata
                            }
        except Exception:
            msg = _("Unable to retrieve profile.")
            url = reverse_lazy(profiles_forms.INDEX_URL)
            exceptions.handle(self.request, msg, redirect=url)
        return profile_dict

    def get_context_data(self, **kwargs):
        args = (self.kwargs["profile_id"],)
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["profile"] = self.get_object()
        context["submit_url"] = reverse_lazy(profiles_forms.UPDATE_URL,
                                             args=args)
        return context

    def get_initial(self):
        return self.get_object()


class DetailView(tabs.TabView):
    tab_group_class = profiles_tabs.ProfileDetailTabs
    template_name = 'horizon/common/_detail.html'
    page_title = "{{ profile.name }}"

    @memoized.memoized_method
    def get_object(self):
        try:
            # Get initial profile information
            profile_id = self.kwargs["profile_id"]
            profile = senlin.profile_get(self.request, profile_id)
            profile.profile_id = profile_id
            profile.profile_spec = yaml.safe_dump(profile.spec,
                                                  default_flow_style=False)
            profile.profile_metadata = yaml.safe_dump(profile.metadata,
                                                      default_flow_style=False)
        except Exception:
            msg = _("Unable to retrieve profile.")
            url = reverse_lazy(profiles_forms.INDEX_URL)
            exceptions.handle(self.request, msg, redirect=url)
        return profile

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        table = ProfilesTable(self.request)
        profile = self.get_object()
        context["actions"] = table.render_row_actions(profile)
        context["profile"] = profile
        context["url"] = reverse_lazy(profiles_forms.INDEX_URL)
        return context

    def get_tabs(self, request, *args, **kwargs):
        profile = self.get_object()
        return self.tab_group_class(request, profile=profile, **kwargs)

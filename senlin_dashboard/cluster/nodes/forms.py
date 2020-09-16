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

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils.memoized import memoized  # noqa: F401

from senlin_dashboard.api import senlin


def _populate_node_params(name, profile_id, cluster_id, role, metadata):
    if not metadata:
        metadata_dict = {}
    else:
        try:
            metadata_dict = yaml.safe_load(metadata)
        except Exception as ex:
            raise Exception(_('The specified metadata is not a valid '
                              'YAML: %s') % ex)
    params = {"name": name,
              "profile_id": profile_id,
              "cluster_id": cluster_id,
              "role": role,
              "metadata": metadata_dict}

    return params


class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Node Name"))
    profile_id = forms.ThemableChoiceField(
        label=_("Profile"),
        help_text=_("Profile used for this node."))
    cluster_id = forms.ThemableChoiceField(
        label=_("Cluster"),
        required=False,
        help_text=_("Cluster for this node."))
    role = forms.CharField(
        max_length=255,
        label=_("Role"),
        required=False,
        help_text=_("Role for this node in the specific cluster."))
    metadata = forms.CharField(
        label=_("Metadata"),
        required=False,
        help_text=_("YAML formatted metadata."),
        widget=forms.Textarea(attrs={'rows': 4}))

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)
        profiles = senlin.profile_list(request)[0]
        self.fields['profile_id'].choices = (
            [("", _("Select Profile"))] + [(profile.id, profile.name)
                                           for profile in profiles])

        clusters = senlin.cluster_list(request)[0]
        self.fields['cluster_id'].choices = (
            [("", _("Select Cluster"))] + [(cluster.id, cluster.name)
                                           for cluster in clusters])

    def handle(self, request, data):
        try:
            params = _populate_node_params(data['name'],
                                           data['profile_id'],
                                           data['cluster_id'],
                                           data['role'],
                                           data['metadata'])

            node = senlin.node_create(request, **params)
            msg = _('Creating node "%s" successfully') % data['name']
            messages.info(request, msg)
            return node
        except Exception:
            redirect = reverse("horizon:cluster:nodes:index")
            exceptions.handle(request,
                              _("Unable to create node."),
                              redirect=redirect)


class UpdateNodeForm(forms.SelfHandlingForm):
    node_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Node Name"))
    profile_id = forms.ThemableChoiceField(
        label=_("Profile"),
        help_text=_("Profile used for this node."))
    role = forms.CharField(
        max_length=255,
        label=_("Role"),
        required=False,
        help_text=_("Role for this node in the specific cluster."))
    metadata = forms.CharField(
        label=_("Metadata"),
        required=False,
        help_text=_("YAML formatted metadata."),
        widget=forms.Textarea(attrs={'rows': 4}))

    def __init__(self, request, *args, **kwargs):
        super(UpdateNodeForm, self).__init__(request, *args, **kwargs)
        profiles = senlin.profile_list(request)[0]
        self.fields['profile_id'].choices = (
            [("", _("Select Profile"))] + [(profile.id, profile.name)
                                           for profile in profiles])

    def handle(self, request, data):
        params = _populate_node_params(data['name'],
                                       data['profile_id'],
                                       None,
                                       data['role'],
                                       data['metadata'])

        del params['cluster_id']
        try:
            node = senlin.node_update(request, data.get('node_id'), **params)
            messages.success(
                request,
                _('Your node %s update request'
                  ' has been accepted for processing.') %
                data['name'])
            return node
        except Exception:
            redirect = reverse("horizon:cluster:nodes:index")
            exceptions.handle(request,
                              _("Unable to update node."),
                              redirect=redirect)
            return False

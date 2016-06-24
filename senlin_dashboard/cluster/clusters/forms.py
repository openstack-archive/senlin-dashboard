# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import six
import yaml

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils.memoized import memoized  # noqa

from senlin_dashboard.api import senlin


INDEX_URL = "horizon:cluster:clusters:index"


class CreateForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Cluster Name"))
    profile_id = forms.ThemableChoiceField(label=_("Profile"))
    min_size = forms.IntegerField(
        label=_("Min Size"),
        required=False,
        initial=0,
        help_text=_("Min size of the cluster. Default to 0."))
    max_size = forms.IntegerField(
        label=_("Max Size"),
        required=False,
        initial=-1,
        help_text=_("Max size of the cluster. Default to -1, "
                    "means unlimited."))
    desired_capacity = forms.IntegerField(
        label=_("Desired Capacity"),
        initial=0,
        help_text=_("Desired capacity of the cluster. Default to 0."))
    # Hide the parent field
    parent = forms.ThemableChoiceField(
        label=_("Parent Cluster"),
        required=False,
        widget=forms.HiddenInput())
    timeout = forms.IntegerField(
        label=_("Timeout"),
        required=False,
        help_text=_("Cluster creation timeout in seconds."))
    metadata = forms.CharField(
        max_length=255,
        label=_("Metadata"),
        required=False,
        help_text=_("YAML formated metadata"),
        widget=forms.Textarea(attrs={'rows': 4}))

    def __init__(self, request, *args, **kwargs):
        super(CreateForm, self).__init__(request, *args, **kwargs)
        profiles = senlin.profile_list(request)
        self.fields['profile_id'].choices = (
            [("", _("Select Profile"))] + [(profile.id, profile.name)
                                           for profile in profiles])

    def handle(self, request, data):
        try:
            # As we hide the parent field, use None here
            data['parent'] = None

            if not data['metadata']:
                metadata = {}
            else:
                try:
                    metadata = yaml.load(data['metadata'])
                except Exception as ex:
                    raise Exception(_('The specified metadata is not a valid '
                                      'YAML format: %s') % six.text_type(ex))
            data['metadata'] = metadata

            cluster = senlin.cluster_create(request, data)
            msg = _('Creating cluster "%s" successfully') % data['name']
            messages.success(request, msg)
            return cluster
        except Exception:
            redirect = reverse(INDEX_URL)
            exceptions.handle(request,
                              _("Unable to create cluster."),
                              redirect=redirect)


class ManagePoliciesForm(forms.SelfHandlingForm):
    cluster_id = forms.CharField(widget=forms.HiddenInput())
    policies = forms.ThemableChoiceField(label=_("Policies"))
    enabled = forms.BooleanField(
        label=_("Enabled"),
        initial=True,
        required=False,
        help_text=_("Whether the policy should be enabled once attached. "
                    "Default to enabled."))

    def __init__(self, request, *args, **kwargs):
        super(ManagePoliciesForm, self).__init__(request, *args, **kwargs)
        cluster_policies = senlin.cluster_policy_list(
            self.request, kwargs['initial']['cluster_id'], {})
        cluster_policies_ids = [policy.id for policy in cluster_policies]
        policies = senlin.policy_list(self.request)
        available_policies = [(policy.id, policy.name) for policy in policies
                              if policy.id not in cluster_policies_ids]
        self.fields['policies'].choices = (
            [("", _("Select Policy"))] + available_policies)

    def handle(self, request, data):
        try:
            params = {"enabled": data.pop('enabled')}
            attach = senlin.cluster_attach_policy(
                request, data["cluster_id"], data['policies'], params)
            msg = _('Attaching policy %(policy)s to cluster '
                    '%(cluster)s.') % {"policy": data['policies'],
                                       "cluster": data['cluster_id']}
            messages.success(request, msg)
            return attach
        except Exception:
            redirect = reverse(INDEX_URL)
            exceptions.handle(request,
                              _("Unable to attach policy."),
                              redirect=redirect)

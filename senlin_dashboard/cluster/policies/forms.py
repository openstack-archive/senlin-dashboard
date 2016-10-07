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

"""
Forms for managing policies.
"""

import six
import yaml

from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from senlin_dashboard.api import senlin

INDEX_URL = "horizon:cluster:policies:index"
CREATE_URL = "horizon:cluster:policies:create"
DETAIL_URL = "horizon:cluster:policies:detail"
UPDATE_URL = "horizon:cluster:policies:update"


class CreatePolicyForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    spec = forms.CharField(
        label=_("Spec"),
        widget=forms.Textarea(attrs={'rows': 6}),
        help_text=_("The spec yaml used to create the policy."))
    cooldown = forms.IntegerField(
        label=_("Cooldown"),
        min_value=0,
        initial=0,
        widget=forms.HiddenInput(),
        help_text=_("An integer indicating the cooldown seconds "
                    "once the policy is effected. Default to 0."))
    level = forms.IntegerField(
        label=_("Level"),
        min_value=0,
        max_value=100,
        initial=0,
        widget=forms.HiddenInput(),
        help_text=_("An integer between 0 and 100 representing the "
                    "enforcement level. Default to 0."))

    def handle(self, request, data):
        try:
            policy_spec = yaml.load(data.get('spec'))
        except Exception as ex:
            raise Exception(_('The specified data is not a valid '
                              'YAML data: %s') % six.text_type(ex))
        args = {
            'name': data.get('name'),
            'spec': policy_spec,
            'cooldown': data.get('cooldown'),
            'level': data.get('level'),
        }

        try:
            policy = senlin.policy_create(request, args)
            messages.success(request,
                             _('Your policy %s has been created.') %
                             args['name'])
            return policy
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to create new policy')
            exceptions.handle(request, msg, redirect=redirect)
            return False


class UpdatePolicyForm(forms.SelfHandlingForm):
    policy_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Name"))

    def handle(self, request, data):
        params = {"name": data.get('name')}

        try:
            senlin.policy_update(request, data.get('policy_id'), params)
            messages.success(request,
                             _('Your policy %s has been updated.') %
                             params['name'])
            return True
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to update policy')
            exceptions.handle(request, msg, redirect=redirect)
            return False

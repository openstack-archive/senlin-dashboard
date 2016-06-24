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
Forms for managing receivers.
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

INDEX_URL = "horizon:cluster:receivers:index"


class CreateReceiverForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    cluster_id = forms.ThemableChoiceField(
        label=_("Cluster"),
        help_text=_("Targeted cluster for this receiver."))
    action = forms.CharField(
        max_length=255,
        label=_("Action"),
        help_text=_("Name or ID of the targeted action to be triggered."))
    type = forms.ThemableChoiceField(
        label=_("Type"),
        initial='webhook',
        help_text=_("Type of the receiver to create. Defailt to webhook"))
    params = forms.CharField(
        label=_("Parameters"),
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text=_("YAML formatted parameters that will be passed to target "
                    "action when the receiver is triggered."))

    def __init__(self, request, *args, **kwargs):
        super(CreateReceiverForm, self).__init__(request, *args, **kwargs)
        clusters = senlin.cluster_list(request)
        self.fields['cluster_id'].choices = (
            [("", _("Select Cluster"))] + [(cluster.id, cluster.name)
                                           for cluster in clusters])

        type_choices = [
            ('', _("Select Type")),
            ("webhook", "webhook"),
        ]
        self.fields['type'].choices = type_choices

    def handle(self, request, data):
        try:
            params = yaml.load(data.get("params"))
        except Exception as ex:
            raise ValidationError(_('The parameters is not a valid '
                                    'YAML formatted: %s') % six.text_type(ex))
        data["params"] = params

        try:
            receiver = senlin.receiver_create(request, data)
            messages.success(
                request,
                _('Your receiver %s has been created successfully.') %
                data['name'])
            return receiver
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to create new receiver')
            exceptions.handle(request, msg, redirect=redirect)
            return False

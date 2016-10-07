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
Views for managing profiles.
"""

import six
import yaml

from senlinclient.common import utils

from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from senlin_dashboard.api import senlin

INDEX_URL = "horizon:cluster:profiles:index"
CREATE_URL = "horizon:cluster:profiles:create"
UPDATE_URL = "horizon:cluster:profiles:update"
DETAIL_URL = "horizon:cluster:profiles:detail"


def _populate_profile_params(name, spec, metadata, id=None):

    if spec is None:
        spec_dict = None
    else:
        try:
            spec_dict = yaml.load(spec)
        except Exception as ex:
            raise ValidationError(_('The specified file is not a valid '
                                    'YAML file: %s') % six.text_type(ex))
        type_name = spec_dict['type']
        if type_name == 'os.heat.stack':
            spec_dict['properties'] = utils.process_stack_spec(
                spec['properties'])
    if not metadata:
        metadata_dict = {}
    else:
        try:
            metadata_dict = yaml.load(metadata)
        except Exception as ex:
            raise ValidationError(_('The specified file is not a valid '
                                    'YAML file: %s') % six.text_type(ex))
    params = {"name": name,
              "spec": spec_dict,
              "metadata": metadata_dict}

    if id is not None:
        params["id"] = id

    return params


class CreateProfileForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    source_type = forms.ThemableChoiceField(
        label=_('Spec Source'),
        required=False,
        choices=[('file', _('File')),
                 ('yaml', _('YAML'))],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'}))
    spec_file = forms.FileField(
        label=_("Spec File"),
        widget=forms.FileInput(attrs={
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-file': _('Spec File')}),
        required=False,
        help_text=_("The spec file used to create the profile."))
    spec_yaml = forms.CharField(
        label=_("Spec YAML"),
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'switched',
            'data-switch-on': 'source',
            'data-source-yaml': _('Spec YAML')}),
        help_text=_("The spec yaml used to create the profile."))
    metadata = forms.CharField(
        label=_("Metadata"),
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text=_("YAML formatted metadata."))

    def clean(self):
        data = super(CreateProfileForm, self).clean()

        spec_file = data.get('spec_file', None)
        spec_yaml = data.get('spec_yaml', None)

        if not spec_file and not spec_yaml:
            raise ValidationError(
                _("A spec file or yaml must be specified."))
        elif spec_file and spec_yaml:
            raise ValidationError(
                _("Can not specify both sepc file and yaml."))
        else:
            return data

    def handle(self, request, data):
        source_type = data.get('source_type')
        if source_type == "yaml":
            spec = data.get("spec_yaml")
        else:
            spec = self.files['spec_file'].read()
        opts = _populate_profile_params(
            name=data.get('name'),
            spec=spec,
            metadata=data.get('metadata')
        )

        try:
            profile = senlin.profile_create(request, opts)
            messages.success(request,
                             _('Your profile %s has been created.') %
                             opts['name'])
            return profile
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to create new profile')
            exceptions.handle(request, msg, redirect=redirect)
            return False


class UpdateProfileForm(forms.SelfHandlingForm):
    profile_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Name"))
    spec = forms.CharField(
        label=_("Spec"),
        widget=forms.Textarea(
            attrs={'rows': 6, 'readonly': 'readonly'}),
        help_text=_('Update the spec of a profile is not allowed'))
    metadata = forms.CharField(
        label=_("Metadata"),
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text=_("YAML formatted metadata."))

    def handle(self, request, data):
        opts = _populate_profile_params(
            id=data.get('profile_id'),
            name=data.get('name'),
            spec=None,
            metadata=data.get('metadata', {})
        )

        try:
            senlin.profile_update(request, data.get('profile_id'), opts)
            messages.success(request,
                             _('Your profile %s has been updated.') %
                             opts['name'])
            return True
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to update profile')
            exceptions.handle(request, msg, redirect=redirect)
            return False

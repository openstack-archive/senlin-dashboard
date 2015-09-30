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

import ast

from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from senlin_dashboard.api import senlin

INDEX_URL = "horizon:cluster:profiles:index"
CREATE_URL = "horizon:cluster:profiles:create"


def _get_profile_type_list(request):
    try:
        prof_types = senlin.profile_type_list(request)
    except Exception:
        msg = _('Unable to get profile type list')
        exceptions.check_message(["Connection", "refused"], msg)
        raise

    return prof_types


def _get_profile_list(request):
    profiles = []
    try:
        profiles = senlin.profile_list(request)
    except Exception:
        msg = _('Unable to get profile list')
        exceptions.check_message(["Connection", "refused"], msg)
        raise

    return profiles


def _parse_dict(name, src):

    dict = None
    if src != '' and src is not None:
        try:
            dict = ast.literal_eval(src)
        except Exception:
            msg = _('Unable to parse %s.') % name
            raise ValidationError(msg)
    return dict


def _profile_dict(name, prof_type, spec,
                  permission, metadata):

    spec_dict = _parse_dict("spec", spec)

    metadata_dict = _parse_dict("metadata", metadata)
    if metadata_dict is None:
        metadata_dict = {}

    return {"name": name,
            "type": prof_type,
            "spec": spec_dict,
            "permission": permission,
            "metadata": metadata_dict,
            }


class CreateProfileForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    prof_type = forms.ChoiceField(
        label=_('Type'),
        widget=forms.SelectWidget(
            transform=lambda x: "%s" % (x.name)))
    spec = forms.CharField(max_length=255,
                           label=_("Spec"),
                           widget=forms.Textarea(attrs={'rows': 6}))
    permission = forms.CharField(max_length=255,
                                 label=_("Permission"),
                                 required=False)
    metadata = forms.CharField(max_length=255,
                               label=_("Metadata"),
                               required=False,
                               widget=forms.Textarea(attrs={'rows': 4}))

    def __init__(self, request, *args, **kwargs):
        super(CreateProfileForm, self).__init__(request, *args, **kwargs)

        prof_types = _get_profile_type_list(self.request)
        self.fields['prof_type'].choices = [(prof_type.name,
                                             prof_type.name)
                                            for prof_type
                                            in prof_types]

    def clean(self):
        data = super(CreateProfileForm, self).clean()

        profiles = _get_profile_list(self.request)

        if profiles is not None and data.get('name') is not None:
            for profile in profiles:
                if profile.name == data.get('name'):
                    msg = _("The name is already used by another profile.")
                    self.errors["name"] = self.error_class([msg])
                    break

        try:
            _parse_dict('spec', data.get('spec'))
        except ValidationError as e:
            self.errors["spec"] = self.error_class([e.messages[0]])

        try:
            _parse_dict('metadata', data.get('metadata'))
        except Exception as e:
            self.errors["metadata"] = self.error_class([e.messages[0]])

        return data

    def handle(self, request, data):
        opts = _profile_dict(name=data.get('name'),
                             prof_type=data.get('prof_type'),
                             spec=data.get('spec'),
                             permission=data.get('permission', ''),
                             metadata=data.get('metadata', {})
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

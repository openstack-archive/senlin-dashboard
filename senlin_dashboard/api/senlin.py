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

import ast
from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon.utils import memoized
from openstack_dashboard.api import base
from senlinclient import client as senlin_client
from senlinclient.common import sdk
from senlinclient.v1 import models

USER_AGENT = 'python-senlinclient'


class Cluster(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_time', 'updated_time',
              'profile_name', 'status_reason']


class Profile(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'created_time', 'updated_time',
              'permission']


class ProfileType(base.APIResourceWrapper):
    _attrs = ['id', 'name']


@memoized.memoized
def senlinclient(request):
    api_version = "1"
    kwargs = {
        'auth_url': getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        'token': request.user.token.id,
        'project_id': request.user.tenant_id
    }
    conn = sdk.create_connection({},
                                 USER_AGENT, **kwargs)

    return senlin_client.Client(api_version, conn.session)


def cluster_list(request):
    """Returns all clusters."""
    clusters = senlinclient(request).list(models.Cluster)
    return [Cluster(c) for c in clusters]


def profile_list(request):
    """Returns all profiles."""
    profiles = senlinclient(request).list(models.Profile)
    return [Profile(p) for p in profiles]


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


def profile_type_list(request):
    """Returns all profile types."""
    prof_types = senlinclient(request).list(models.ProfileType)
    return [ProfileType(t) for t in prof_types]


def profile_create(request, opts):
    """Create profile."""
    profile = senlinclient(request).create(models.Profile, opts)
    return profile


def profile_delete(request, profile_id):
    """Delete profile."""
    senlinclient(request).delete(models.Profile, {"id": profile_id})

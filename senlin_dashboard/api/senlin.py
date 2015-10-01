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

from django.conf import settings

from horizon.utils import memoized
from openstack_dashboard.api import base
from senlinclient import client as senlin_client
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


class Policy(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'spec', 'level', 'cooldown',
              'created_time', 'updated_time']


class Node(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_time', 'updated_time',
              'profile_name', 'status_reason', 'physical_id', 'role']


@memoized.memoized
def senlinclient(request):
    api_version = "1"
    kwargs = {
        'auth_url': getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        'token': request.user.token.id,
        'project_id': request.user.tenant_id
    }
    return senlin_client.Client(api_version, {}, USER_AGENT, **kwargs)


def cluster_list(request):
    """Returns all clusters."""
    clusters = senlinclient(request).list(models.Cluster)
    return [Cluster(c) for c in clusters]


def profile_list(request):
    """Returns all profiles."""
    profiles = senlinclient(request).list(models.Profile)
    return [Profile(p) for p in profiles]


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


def policy_list(request):
    """Returns all policies."""
    policies = senlinclient(request).list(models.Policy)
    return [Policy(p) for p in policies]


def node_list(request):
    """Returns all nodes."""
    nodes = senlinclient(request).list(models.Node)
    return [Node(p) for p in nodes]

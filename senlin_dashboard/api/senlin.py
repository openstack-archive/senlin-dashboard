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

USER_AGENT = 'python-senlinclient'


class Cluster(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_at', 'updated_at',
              'profile_name', 'profile_id', 'status_reason']


class ClusterPolicy(base.APIResourceWrapper):
    _attrs = ['id', 'policy_name', 'policy_type', 'enabled',
              'cluster_id']


class Profile(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type_name', 'created_at', 'updated_at',
              'metadata', 'spec']


class ProfileType(base.APIResourceWrapper):
    _attrs = ['id', 'name']


class Policy(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'spec', 'level', 'cooldown',
              'created_at', 'updated_at']


class Node(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_at', 'updated_at',
              'profile_name', 'status_reason', 'physical_id', 'role',
              'profile_id', 'profile_url', 'cluster_id']


class Event(base.APIResourceWrapper):
    _attrs = ['id', 'obj_id', 'obj_name', 'timestamp', 'status',
              'status_reason', 'action']


class Receiver(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'cluster_id', 'action', 'created_at',
              'updated_at', 'channel']


@memoized.memoized
def senlinclient(request):
    api_version = "1"
    kwargs = {
        'auth_url': getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        'token': request.user.token.id,
        'user_id': request.user.id,
        'project_id': request.user.tenant_id,
        'auth_plugin': 'token',
    }
    return senlin_client.Client(api_version, {}, USER_AGENT, **kwargs)


def cluster_list(request, params):
    """Returns all clusters."""
    clusters = senlinclient(request).clusters(**params)
    return [Cluster(c) for c in clusters]


def cluster_create(request, params):
    """Create cluster."""
    cluster = senlinclient(request).create_cluster(**params)
    return Cluster(cluster)


def cluster_delete(request, cluster):
    """Delete cluster."""
    senlinclient(request).delete_cluster(cluster)


def cluster_get(request, cluster):
    """Returns cluster."""
    cluster = senlinclient(request).get_cluster(cluster)
    return Cluster(cluster)


def cluster_attach_policy(request, cluster, policy, params):
    """Attach policy to a specific cluster"""
    return senlinclient(request).cluster_attach_policy(
        cluster, policy, **params)


def cluster_detach_policy(request, cluster, policy):
    """Detach policy from cluster."""
    senlinclient(request).cluster_detach_policy(
        cluster, policy)


def cluster_policy_list(request, cluster, params):
    """List policies from cluster."""
    policies = senlinclient(request).cluster_policies(
        cluster, **params)
    return [ClusterPolicy(p) for p in policies]


def profile_list(request, params):
    """Returns all profiles."""
    profiles = senlinclient(request).profiles(**params)
    return [Profile(p) for p in profiles]


def profile_get(request, profile):
    """Returns profile."""
    profile = senlinclient(request).get_profile(profile)
    return Profile(profile)


def profile_create(request, params):
    """Create profile."""
    profile = senlinclient(request).create_profile(**params)
    return Profile(profile)


def profile_update(request, profile, params):
    """Update profile."""
    profile = senlinclient(request).update_profile(profile, **params)
    return Profile(profile)


def profile_delete(request, profile):
    """Delete profile."""
    senlinclient(request).delete_profile(profile)


def policy_list(request, params):
    """Returns all policies."""
    policies = senlinclient(request).policies(**params)
    return [Policy(p) for p in policies]


def policy_create(request, params):
    """Create a policy."""
    policy = senlinclient(request).create_policy(**params)
    return policy


def policy_delete(request, policy):
    """Delete a policy."""
    senlinclient(request).delete_policy(policy)


def policy_get(request, policy):
    """Returns policy."""
    policy = senlinclient(request).get_policy(policy)
    return policy


def node_list(request, params):
    """Returns all nodes."""
    nodes = senlinclient(request).nodes(**params)
    return [Node(p) for p in nodes]


def node_create(request, params):
    """Create node."""
    node = senlinclient(request).create_node(**params)
    return node


def node_delete(request, node):
    """Delete node."""
    senlinclient(request).delete_node(node)


def node_get(request, node):
    """Returns node."""
    node = senlinclient(request).get_node(node)
    return Node(node)


def event_list(request, params):
    """Returns events."""
    events = senlinclient(request).events(**params)
    return [Event(c) for c in events]


def receiver_list(request, params):
    receivers = senlinclient(request).receivers(**params)
    return [Receiver(r) for r in receivers]


def receiver_create(request, params):
    """Create receiver"""
    receiver = senlinclient(request).create_receiver(**params)
    return Receiver(receiver)


def receiver_delete(request, receiver):
    """Delete receiver."""
    senlinclient(request).delete_receiver(receiver)


def receiver_get(request, receiver):
    receiver = senlinclient(request).get_receiver(receiver)
    return Receiver(receiver)

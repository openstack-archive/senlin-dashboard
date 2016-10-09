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

from horizon.utils import functions as utils
from horizon.utils import memoized

from openstack_dashboard.api import base
from senlin_dashboard.api import utils as api_utils
from senlinclient import client as senlin_client

USER_AGENT = 'python-senlinclient'


class Cluster(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_at', 'updated_at',
              'profile_name', 'profile_id', 'status_reason',
              'max_size', 'min_size', 'desired_capacity', 'timeout',
              'metadata']


class ClusterPolicy(base.APIResourceWrapper):
    _attrs = ['id', 'policy_name', 'policy_type', 'enabled',
              'cluster_id']


class Profile(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'created_at', 'updated_at',
              'metadata', 'spec']


class ProfileType(base.APIResourceWrapper):
    _attrs = ['id', 'name']


class Policy(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'type', 'spec', 'level', 'cooldown',
              'created_at', 'updated_at']


class Node(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'status', 'created_at', 'updated_at',
              'profile_name', 'status_reason', 'physical_id', 'role',
              'profile_id', 'profile_url', 'cluster_id', 'metadata']


class Event(base.APIResourceWrapper):
    _attrs = ['id', 'obj_id', 'obj_name', 'generated_at', 'status',
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


def _populate_request_size_and_page_size(request, paginate=False):
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    return page_size, request_size


def cluster_list(request, sort_dir='desc', sort_key='created_at',
                 marker=None, paginate=False, reversed_order=False,
                 filters=None):
    """Returns all clusters."""

    page_size, request_size = _populate_request_size_and_page_size(
        request, paginate)

    if not filters:
        filters = {}

    if reversed_order:
        sort_dir = 'desc' if sort_dir == 'asc' else 'asc'

    params = {
        'sort': '%s:%s' % (sort_key, sort_dir),
        'limit': request_size,
        'marker': marker}

    params.update(filters)

    clusters_iter = senlinclient(request).clusters(**params)

    if paginate:
        clusters, has_more_data, has_prev_data = api_utils.update_pagination(
            clusters_iter, request_size, page_size, marker,
            sort_dir, sort_key, reversed_order)

        return [Cluster(p) for p in clusters], has_more_data, has_prev_data
    else:
        clusters = list(clusters_iter)
        return [Cluster(p) for p in clusters]


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


def profile_list(request, sort_dir='desc', sort_key='created_at',
                 marker=None, paginate=False, reversed_order=False,
                 filters=None):
    """Returns all profiles."""

    page_size, request_size = _populate_request_size_and_page_size(
        request, paginate)

    if not filters:
        filters = {}

    params = {
        'sort': '%s:%s' % (sort_key, sort_dir),
        'limit': request_size,
        'marker': marker}

    params.update(filters)

    profiles_iter = senlinclient(request).profiles(**params)

    if paginate:
        profiles, has_more_data, has_prev_data = api_utils.update_pagination(
            profiles_iter, request_size, page_size, marker,
            sort_dir, sort_key, reversed_order)

        return [Profile(p) for p in profiles], has_more_data, has_prev_data
    else:
        profiles = list(profiles_iter)
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


def policy_list(request, sort_dir='desc', sort_key='created_at',
                marker=None, paginate=False, reversed_order=False,
                filters=None):
    """Returns all policies."""

    page_size, request_size = _populate_request_size_and_page_size(
        request, paginate)

    if not filters:
        filters = {}

    if reversed_order:
        sort_dir = 'desc' if sort_dir == 'asc' else 'asc'

    params = {
        'sort': '%s:%s' % (sort_key, sort_dir),
        'limit': request_size,
        'marker': marker}

    params.update(filters)

    policies_iter = senlinclient(request).policies(**params)

    if paginate:
        policies, has_more_data, has_prev_data = api_utils.update_pagination(
            policies_iter, request_size, page_size, marker,
            sort_dir, sort_key, reversed_order)

        return [Policy(p) for p in policies], has_more_data, has_prev_data
    else:
        policies = list(policies_iter)
        return [Policy(p) for p in policies]


def policy_create(request, params):
    """Create a policy."""
    policy = senlinclient(request).create_policy(**params)
    return policy


def policy_update(request, policy, params):
    """Update policy."""
    policy = senlinclient(request).update_policy(policy, **params)
    return Policy(policy)


def policy_delete(request, policy):
    """Delete a policy."""
    senlinclient(request).delete_policy(policy)


def policy_get(request, policy):
    """Returns policy."""
    policy = senlinclient(request).get_policy(policy)
    return policy


def node_list(request, sort_dir='desc', sort_key='name',
              marker=None, paginate=False, reversed_order=False,
              cluster_id=None, filters=None):
    """Returns all nodes."""

    # NOTE(Liuqing): workaround for bug: 1594352
    # https://bugs.launchpad.net/senlin/+bug/1594352
    # Sometimes we failed to create node and the `created_at` attribution
    # node object will be None. The api node_list will failed if we
    # use `created_at` as the `sort_key`.

    page_size, request_size = _populate_request_size_and_page_size(
        request, paginate)

    if not filters:
        filters = {}

    if reversed_order:
        sort_dir = 'desc' if sort_dir == 'asc' else 'asc'

    params = {
        'sort': '%s:%s' % (sort_key, sort_dir),
        'limit': request_size,
        'marker': marker,
        'cluster_id': cluster_id}

    params.update(filters)

    nodes_iter = senlinclient(request).nodes(**params)

    if paginate:
        nodes, has_more_data, has_prev_data = api_utils.update_pagination(
            nodes_iter, request_size, page_size, marker,
            sort_dir, sort_key, reversed_order)

        return [Node(n) for n in nodes], has_more_data, has_prev_data
    else:
        nodes = list(nodes_iter)
        return [Node(n) for n in nodes]


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


def node_update(request, node, params):
    """Update node"""
    node = senlinclient(request).update_node(node, **params)
    return node


def event_list(request, params):
    """Returns events."""
    events = senlinclient(request).events(**params)
    return [Event(c) for c in events]


def receiver_list(request, sort_dir='desc', sort_key='created_at',
                  marker=None, paginate=False, reversed_order=False,
                  filters=None):
    """Returns all receivers."""

    has_prev_data = False
    has_more_data = False

    page_size, request_size = _populate_request_size_and_page_size(
        request, paginate)

    if not filters:
        filters = {}

    if reversed_order:
        sort_dir = 'desc' if sort_dir == 'asc' else 'asc'

    params = {
        'sort': '%s:%s' % (sort_key, sort_dir),
        'limit': request_size,
        'marker': marker}

    params.update(filters)

    receivers_iter = senlinclient(request).receivers(**params)

    if paginate:
        receivers, has_more_data, has_prev_data = api_utils.update_pagination(
            receivers_iter, request_size, page_size, marker,
            sort_dir, sort_key, reversed_order)
    else:
        receivers = list(receivers_iter)

    return [Receiver(r) for r in receivers], has_more_data, has_prev_data


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

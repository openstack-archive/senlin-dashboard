# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API for the senlin service."""

from django.views import generic

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from senlin_dashboard.api import senlin
from senlin_dashboard.api import utils as api_utils
from senlin_dashboard.cluster.nodes import forms as node_forms
from senlin_dashboard.cluster.policies import forms as policy_forms
from senlin_dashboard.cluster.profiles import forms
from senlin_dashboard.cluster.receivers import forms as receiver_forms

CLIENT_KEYWORDS = {'marker', 'sort_dir', 'sort_key', 'paginate'}


@urls.register
class Receivers(generic.View):
    """API for Senlin receiver."""

    url_regex = r'senlin/receivers/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of receivers."""

        filters, kwargs = rest_utils.parse_filters_kwargs(request,
                                                          CLIENT_KEYWORDS)

        receivers, has_more_data, has_prev_data = senlin.receiver_list(
            request, filters=filters, **kwargs)

        receivers_dict = []
        for r in receivers:
            r = r.to_dict()
            r["params"] = api_utils.convert_to_yaml(r["params"])
            r["channel"] = api_utils.convert_to_yaml(r["channel"])
            receivers_dict.append(r)

        return {
            'items': receivers_dict,
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Receiver.

        Returns the new Receiver object on success.
        """
        request_param = request.DATA
        params = receiver_forms._populate_receiver_params(
            request_param.get("name"),
            request_param.get("type"),
            request_param.get("cluster_id"),
            request_param.get("action"),
            request_param.get("params"))
        new_receiver = senlin.receiver_create(request, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/receivers/%s' % new_receiver.id,
            new_receiver.to_dict())


@urls.register
class Receiver(generic.View):
    """API for Senlin receiver."""

    url_regex = r'senlin/receivers/(?P<receiver_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, receiver_id):
        """Get a single receiver's details with the receiver id.

        The following get parameters may be passed in the GET

        :param receiver_id: the id of the receiver

        The result is a receiver object.
        """
        receiver = senlin.receiver_get(request, receiver_id).to_dict()
        receiver["params"] = api_utils.convert_to_yaml(receiver["params"])
        receiver["channel"] = api_utils.convert_to_yaml(receiver["channel"])
        return receiver

    @rest_utils.ajax(data_required=True)
    def put(self, request, receiver_id):
        """Update a Profile.

        Returns the Profile object on success.
        """
        request_param = request.DATA
        params = receiver_forms._populate_receiver_params(
            request_param.get("name"),
            None,
            None,
            request_param.get("action"),
            request_param.get("params"))
        del params['type']
        del params['cluster_id']
        updated_receiver = senlin.receiver_update(
            request, receiver_id, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/receivers/%s' % updated_receiver.id,
            updated_receiver.to_dict())

    @rest_utils.ajax()
    def delete(self, request, receiver_id):
        """Delete a specific receiver

        DELETE http://localhost/api/senlin/receivers/cc758c90-3d98-4ea1-af44-aab405c9c915  # noqa
        """
        senlin.receiver_delete(request, receiver_id)


@urls.register
class Profiles(generic.View):
    """API for Senlin profile."""

    url_regex = r'senlin/profiles/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of profiles."""

        filters, kwargs = rest_utils.parse_filters_kwargs(request,
                                                          CLIENT_KEYWORDS)

        profiles, has_more_data, has_prev_data = senlin.profile_list(
            request, filters=filters, **kwargs)

        return {
            'items': [p.to_dict() for p in profiles],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Profile.

        Returns the new Profile object on success.
        """
        request_param = request.DATA
        params = forms._populate_profile_params(request_param.get("name"),
                                                request_param.get("spec"),
                                                request_param.get("metadata"))
        new_profile = senlin.profile_create(request, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/profiles/%s' % new_profile.id,
            new_profile.to_dict())


@urls.register
class Profile(generic.View):
    """API for Senlin profile."""

    url_regex = r'senlin/profiles/(?P<profile_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, profile_id):
        """Get a single profile's details with the profile id.

        The following get parameters may be passed in the GET

        :param profile_id: the id of the profile

        The result is a profile object.
        """
        profile = senlin.profile_get(request, profile_id).to_dict()
        profile["spec"] = api_utils.convert_to_yaml(profile["spec"])
        profile["metadata"] = api_utils.convert_to_yaml(profile["metadata"])
        return profile

    @rest_utils.ajax(data_required=True)
    def put(self, request, profile_id):
        """Update a Profile.

        Returns the Profile object on success.
        """
        request_param = request.DATA
        params = forms._populate_profile_params(request_param.get("name"),
                                                None,
                                                request_param.get("metadata"))
        del params['spec']
        updated_profile = senlin.profile_update(
            request, profile_id, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/profiles/%s' % updated_profile.id,
            updated_profile.to_dict())

    @rest_utils.ajax()
    def delete(self, request, profile_id):
        """Delete a specific profile

        DELETE http://localhost/api/senlin/profiles/cc758c90-3d98-4ea1-af44-aab405c9c915  # noqa
        """
        senlin.profile_delete(request, profile_id)


@urls.register
class Nodes(generic.View):
    """API for Senlin node."""

    url_regex = r'senlin/nodes/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of nodes."""

        filters, kwargs = rest_utils.parse_filters_kwargs(request,
                                                          CLIENT_KEYWORDS)

        nodes, has_more_data, has_prev_data = senlin.node_list(
            request, filters=filters, **kwargs)

        return {
            'items': [n.to_dict() for n in nodes],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Node.

        Returns the new Node object on success.
        """
        request_param = request.DATA
        params = node_forms._populate_node_params(
            request_param.get("name"),
            request_param.get("profile_id"),
            request_param.get("cluster_id"),
            request_param.get("role"),
            request_param.get("metadata"))
        new_node = senlin.node_create(request, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/nodes/%s' % new_node.id,
            new_node.to_dict())


@urls.register
class Node(generic.View):
    """API for Senlin node."""

    url_regex = r'senlin/nodes/(?P<node_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, node_id):
        """Get a single node's details with the receiver id.

        The following get parameters may be passed in the GET

        :param node_id: the id of the node

        The result is a node object.
        """
        node = senlin.node_get(request, node_id).to_dict()
        node["metadata"] = api_utils.convert_to_yaml(node["metadata"])
        return node

    @rest_utils.ajax()
    def delete(self, request, node_id):
        """Delete a specific node

        DELETE http://localhost/api/senlin/nodes/cc758c90-3d98-4ea1-af44-aab405c9c915  # noqa
        """
        senlin.node_delete(request, node_id)

    @rest_utils.ajax(data_required=True)
    def put(self, request, node_id):
        """Update a Node.

        Returns the Node object on success.
        """
        request_param = request.DATA
        params = node_forms._populate_node_params(
            request_param.get("name"),
            request_param.get("profile_id"),
            None,
            request_param.get("role"),
            request_param.get("metadata"))
        params.pop('cluster_id')
        updated_node = senlin.node_update(
            request, node_id, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/nodes/%s' % updated_node.id,
            updated_node.to_dict())


@urls.register
class Events(generic.View):
    """API for Senlin events."""

    url_regex = r'senlin/events/(?P<obj_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, obj_id):
        """Get a list of events."""

        events, has_more_data, has_prev_data = senlin.event_list(
            request, filters={"obj_id": obj_id}, paginate=False)

        return {
            'items': [e.to_dict() for e in events],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }


@urls.register
class Clusters(generic.View):
    """API for Senlin cluster."""

    url_regex = r'senlin/clusters/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of clusters."""

        filters, kwargs = rest_utils.parse_filters_kwargs(request,
                                                          CLIENT_KEYWORDS)

        clusters, has_more_data, has_prev_data = senlin.cluster_list(
            request, filters=filters, **kwargs)

        return {
            'items': [c.to_dict() for c in clusters],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Cluster.

        Returns the new Cluster object on success.
        """
        params = request.DATA
        params["metadata"] = api_utils.load_yaml(params.get("metadata"))
        cluster = senlin.cluster_create(request, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/clusters/%s' % cluster.id, cluster.to_dict())


@urls.register
class Cluster(generic.View):
    """API for Senlin cluster."""

    url_regex = r'senlin/clusters/(?P<cluster_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, cluster_id):
        """Get a single cluster's details with the cluster id.

        The following get parameters may be passed in the GET

        :param cluster_id: the id of the cluster

        The result is a cluster object.
        """
        cluster = senlin.cluster_get(request, cluster_id).to_dict()
        cluster["metadata"] = api_utils.convert_to_yaml(cluster["metadata"])
        return cluster

    @rest_utils.ajax()
    def delete(self, request, cluster_id):
        """Delete a specific cluster

        DELETE http://localhost/api/senlin/clusters/cc758c90-3d98-4ea1-af44-aab405c9c915  # noqa
        """
        senlin.cluster_delete(request, cluster_id)

    @rest_utils.ajax(data_required=True)
    def put(self, request, cluster_id):
        """Update a Cluster.

        Returns the Cluster object on success.
        """
        params = request.DATA
        params["metadata"] = api_utils.load_yaml(params.get("metadata"))
        updated_cluster = senlin.cluster_update(
            request, cluster_id, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/clusters/%s' % updated_cluster.id,
            updated_cluster.to_dict())


@urls.register
class ClusterActions(generic.View):
    """API for Senlin cluster."""

    url_regex = r'senlin/clusters/(?P<cluster_id>[^/]+)/(?P<action>[^/]+)$'

    @rest_utils.ajax()
    def get(self, request, cluster_id, action):
        if action == "policy":
            """Get policies of a single cluster with the cluster id.

            The following get parameters may be passed in the GET

            :param cluster_id: the id of the cluster

            The result is a cluster object.
            """
            policies = senlin.cluster_policy_list(request, cluster_id, {})

            return {
                'items': [p.to_dict() for p in policies],
            }
        elif action == "":
            return None

    @rest_utils.ajax(data_required=True)
    def put(self, request, cluster_id, action):
        if action == "policy":
            """Update policies for the cluster."""
            params = request.DATA

            new_attach_ids = params["ids"]
            old_attached = senlin.cluster_policy_list(request, cluster_id, {})

            # Extract policies should be detached and execute
            for policy in old_attached:
                should_detach = True
                for new_id in new_attach_ids:
                    if new_id == policy.policy_id:
                        # This policy is already attached.
                        should_detach = False
                        break
                if should_detach:
                    # If policy is not exist in new policies,
                    # it should be removed
                    senlin.cluster_detach_policy(
                        request, cluster_id, policy.policy_id)

            # Extract policies should be attached and execute
            for new_id in new_attach_ids:
                should_attach = True
                for policy in old_attached:
                    if new_id == policy.policy_id:
                        # This policy is already attached.
                        should_attach = False
                        break
                if should_attach:
                    # If policy is not exist in old policies,
                    # it should be added
                    senlin.cluster_attach_policy(request, cluster_id,
                                                 new_id, {})

            return rest_utils.CreatedResponse(
                '/api/senlin/clusters/%s/policy' % cluster_id)
        elif action == "scale-in":
            count = request.DATA.get("count") or None
            return senlin.cluster_scale_in(request, cluster_id, count)
        elif action == "scale-out":
            count = request.DATA.get("count") or None
            return senlin.cluster_scale_out(request, cluster_id, count)
        elif action == "resize":
            params = request.DATA
            return senlin.cluster_resize(request, cluster_id, **params)


@urls.register
class Policies(generic.View):
    """API for Senlin policies."""

    url_regex = r'senlin/policies/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of policies."""

        filters, kwargs = rest_utils.parse_filters_kwargs(request,
                                                          CLIENT_KEYWORDS)
        policies, has_more_data, has_prev_data = senlin.policy_list(
            request, filters=filters, **kwargs)

        return {
            'items': [p.to_dict() for p in policies],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a new Policy.

        Returns the new Policy object on success.
        """
        request_param = request.DATA
        params = policy_forms._populate_policy_params(
            request_param.get("name"),
            request_param.get("spec"),
            request_param.get("cooldown"),
            request_param.get("level"))
        new_policy = senlin.policy_create(request, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/policies/%s' % new_policy.id,
            new_policy.to_dict())


@urls.register
class Policy(generic.View):
    """API for Senlin policy."""

    url_regex = r'senlin/policies/(?P<policy_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, policy_id):
        """Get a single policy's details with the policy id.

        The following get parameters may be passed in the GET

        :param policy_id: the id of the policy

        The result is a policy object.
        """
        policy = senlin.policy_get(request, policy_id).to_dict()
        policy["spec"] = api_utils.convert_to_yaml(policy["spec"])
        return policy

    @rest_utils.ajax()
    def delete(self, request, policy_id):
        """Delete a specific policy

        DELETE http://localhost/api/senlin/policies/cc758c90-3d98-4ea1-af44-aab405c9c915  # noqa
        """
        senlin.policy_delete(request, policy_id)

    @rest_utils.ajax(data_required=True)
    def put(self, request, policy_id):
        """Update a Policy.

        Returns the Policy object on success.
        """
        request_param = request.DATA
        params = policy_forms._populate_policy_params(
            request_param.get("name"),
            None, None, None)
        params.pop('spec')
        params.pop('cooldown')
        params.pop('level')
        updated_policy = senlin.policy_update(
            request, policy_id, **params)
        return rest_utils.CreatedResponse(
            '/api/senlin/policies/%s' % updated_policy.id,
            updated_policy.to_dict())

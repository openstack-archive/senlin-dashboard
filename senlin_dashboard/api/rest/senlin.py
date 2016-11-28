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
from senlin_dashboard.cluster.profiles import forms


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

        return {
            'items': [r.to_dict() for r in receivers],
            'has_more_data': has_more_data,
            'has_prev_data': has_prev_data,
        }


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
        return senlin.receiver_get(request, receiver_id).to_dict()

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
        return senlin.profile_get(request, profile_id).to_dict()

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
        return senlin.cluster_get(request, cluster_id).to_dict()

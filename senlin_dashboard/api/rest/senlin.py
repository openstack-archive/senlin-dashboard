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

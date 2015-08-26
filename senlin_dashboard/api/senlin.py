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

from horizon.utils import memoized
from openstack_dashboard.api import base
from senlinclient import client as senlin_client
from senlinclient.common import sdk

USER_AGENT = 'python-senlinclient'


@memoized.memoized
def senlinclient(request, password=None):
    api_version = "1"
    kwargs = {
        'auth_url': base.url_for(request, 'clustering'),
        'token': request.user.token.id,
        'project_id': request.user.tenant_id
    }
    conn = sdk.create_connection({},
                                 USER_AGENT, **kwargs)

    return senlin_client.Client(api_version, conn.session)

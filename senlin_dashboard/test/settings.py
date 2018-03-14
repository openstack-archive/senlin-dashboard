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

from horizon.test.settings import *  # noqa: F403,H303
from openstack_dashboard.test.settings import *  # noqa: F403,H303

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('senlin_dashboard.cluster')

# NOTE(shu-mutou): For Django-based panels. This should be remove when
# deprecated Django-based panels are removed.
ANGULAR_FEATURES.update({
    'profiles_panel': False,
    'nodes_panel': False,
    'clusters_panel': False,
    'policies_panel': False,
    'receivers_panel': False
})

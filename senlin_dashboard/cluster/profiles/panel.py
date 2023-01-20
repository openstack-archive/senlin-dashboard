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

from django.utils.translation import gettext_lazy as _

import horizon

# import REST API modules here
from senlin_dashboard.api.rest import senlin  # noqa: F401
from senlin_dashboard.cluster import dashboard


class Profiles(horizon.Panel):
    name = _("Profiles")
    slug = 'profiles'


dashboard.Cluster.register(Profiles)

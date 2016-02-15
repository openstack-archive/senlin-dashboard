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

from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.utils import filters


def get_updated_time(object):
    return filters.parse_isotime(object.updated_at) or None


class ReceiversTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    type = tables.Column("type", verbose_name=_("Type"))
    cluster_id = tables.Column("cluster_id", verbose_name=_("Cluster ID"))
    action = tables.Column("action", verbose_name=_("Action"))
    created = tables.Column(
        "created_at",
        verbose_name=_("Created"),
        filters=(
            filters.parse_isotime,
        )
    )
    updated = tables.Column(
        get_updated_time,
        verbose_name=_("Updated"),
    )

    class Meta(object):
        name = "receivers"
        verbose_name = _("Receivers")
        table_actions = (tables.FilterAction,)

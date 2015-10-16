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
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon.utils import filters

from senlin_dashboard import api


class CreateNode(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Node")
    url = "horizon:cluster:nodes:create"
    classes = ("ajax-modal", "btn-create")
    icon = "plus"
    ajax = True


class DeleteNode(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Node",
            u"Delete Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Node",
            u"Deleted Nodes",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.node_delete(request, obj_id)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, node_id):
        node = api.senlin.node_get(request, node_id)
        return node


class NodesTable(tables.DataTable):
    STATUS_CHOICES = (
        ("ACTIVE", True),
        ("ERROR", False),
    )

    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:cluster:nodes:detail")
    profile_name = tables.Column("profile_name",
                                 verbose_name=_("Profile Name"))
    physical_id = tables.Column("physical_id", verbose_name=_("Physical ID"))
    role = tables.Column("role", verbose_name=_("Role"))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES)
    status_reason = tables.Column("status_reason",
                                  verbose_name=_("Status Reason"))
    created = tables.Column(
        "created_time",
        verbose_name=_("Created"),
        filters=(
            filters.parse_isotime,
            filters.timesince_or_never
        )
    )
    updated = tables.Column(
        "updated_time",
        verbose_name=_("Updated"),
        filters=(
            filters.parse_isotime,
            filters.timesince_or_never
        )
    )

    class Meta(object):
        name = "nodes"
        row_class = UpdateRow
        verbose_name = _("Nodes")
        status_columns = ["status"]
        table_actions = (tables.FilterAction,
                         CreateNode,
                         DeleteNode,)
        row_actions = (DeleteNode,)

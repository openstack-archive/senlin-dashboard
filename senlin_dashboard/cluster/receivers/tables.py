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

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon.utils import filters

from senlin_dashboard import api


class CreateReceiver(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Receiver")
    url = "horizon:cluster:receivers:create"
    classes = ("ajax-modal", "btn-create")
    icon = "plus"
    ajax = True


class DeleteReceiver(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Receiver",
            u"Delete Receivers",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Receiver",
            u"Deleted Receivers",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.receiver_delete(request, obj_id)


def get_updated_time(object):
    return object.updated_at or None


def get_cluster_link(receiver):
    if receiver.cluster_id:
        return reverse_lazy('horizon:cluster:clusters:detail',
                            args=[receiver.cluster_id])


class ReceiverFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (
        ("name", _("Receiver Name ="), True),
        ("type", _("Type ="), True),
        ("action", _("Action ="), True),
        ("cluster_id", _("Cluster ID ="), True),
    )


class ReceiversTable(tables.DataTable):
    name = tables.WrappingColumn(
        "name",
        verbose_name=_("Name"),
        link="horizon:cluster:receivers:detail")
    type = tables.Column("type", verbose_name=_("Type"))
    cluster_id = tables.Column('cluster_id',
                               link=get_cluster_link,
                               verbose_name=_("Cluster ID"))
    action = tables.Column("action", verbose_name=_("Action"))
    created = tables.Column(
        "created_at",
        verbose_name=_("Created"),
        filters=(filters.parse_isotime,)
    )
    updated = tables.Column(
        get_updated_time,
        verbose_name=_("Updated"),
        filters=(filters.parse_isotime,)
    )

    class Meta(object):
        name = "receivers"
        verbose_name = _("Receivers")
        table_actions = (ReceiverFilterAction,
                         CreateReceiver,
                         DeleteReceiver,)
        row_actions = (DeleteReceiver,)

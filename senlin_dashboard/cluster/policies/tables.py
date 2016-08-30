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

from senlin_dashboard import api
from senlin_dashboard.cluster.policies import forms as policies_forms


class CreatePolicy(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Policy")
    url = policies_forms.CREATE_URL
    classes = ("ajax-modal",)
    icon = "plus"


class DeletePolicy(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Policy",
            u"Delete Policies",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Policy",
            u"Deleted Policies",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.policy_delete(request, obj_id)


def get_updated_time(object):
    return object.updated_at or None


class PoliciesTable(tables.DataTable):
    name = tables.WrappingColumn(
        "name",
        verbose_name=_("Name"),
        link=policies_forms.DETAIL_URL)
    type = tables.Column("type", verbose_name=_("Type"))
    created = tables.Column(
        "created_at",
        verbose_name=_("Created"),
    )
    updated = tables.Column(
        get_updated_time,
        verbose_name=_("Updated"),
    )

    class Meta(object):
        name = "policies"
        verbose_name = _("Policies")
        table_actions = (tables.FilterAction,
                         CreatePolicy,
                         DeletePolicy,)
        row_actions = (DeletePolicy,)

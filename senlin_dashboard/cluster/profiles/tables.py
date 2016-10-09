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
from senlin_dashboard.cluster.profiles import forms as profiles_forms


class CreateProfile(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Profile")
    url = profiles_forms.CREATE_URL
    classes = ("ajax-modal",)
    icon = "plus"


class UpdateProfile(tables.LinkAction):
    name = "update"
    verbose_name = _("Update Profile")
    url = profiles_forms.UPDATE_URL
    classes = ("ajax-modal",)
    icon = "pencil"


class DeleteProfile(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Profile",
            u"Delete Profiles",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Profile",
            u"Deleted Profiles",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.profile_delete(request, obj_id)


def get_updated_time(object):
    return object.updated_at or None


def get_profile_name(profile):
    return getattr(profile, "name").strip() or profile.id


class ProfileFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (
        ("name", _("Profile Name ="), True),
    )


class ProfilesTable(tables.DataTable):
    name = tables.WrappingColumn(
        get_profile_name,
        verbose_name=_("Name"),
        link=profiles_forms.DETAIL_URL)
    type = tables.Column("type", verbose_name=_("Type"))
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
        name = "profiles"
        verbose_name = _("Profiles")
        table_actions = (ProfileFilterAction,
                         CreateProfile,
                         DeleteProfile)
        row_actions = (UpdateProfile, DeleteProfile,)

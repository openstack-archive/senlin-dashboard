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

from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.utils import filters


class EventsTable(tables.DataTable):
    STATUS_CHOICES = (
        ("INIT", None),
        ("ACTIVE", True),
        ("ERROR", False),
        ("DELETED", False),
        ("WARNING", None),
        ("CREATING", None),
        ("UPDATING", None),
        ("DELETING", None),
    )

    STATUS_DISPLAY_CHOICES = (
        ("INIT", pgettext_lazy("Current status of the event", u"INIT")),
        ("ACTIVE", pgettext_lazy("Current status of the event", u"ACTIVE")),
        ("ERROR", pgettext_lazy("Current status of the event", u"ERROR")),
        ("DELETED", pgettext_lazy("Current status of the event", u"DELETED")),
        ("WARNING", pgettext_lazy("Current status of the event", u"WARNING")),
        ("CREATING",
         pgettext_lazy("Current status of the event", u"CREATING")),
        ("UPDATING",
         pgettext_lazy("Current status of the event", u"UPDATING")),
        ("DELETING",
         pgettext_lazy("Current status of the event", u"DELETING")),
    )

    obj_id = tables.Column("obj_id", verbose_name=_("Object ID"))
    obj_name = tables.Column("obj_name", verbose_name=_("Object Name"))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)
    status_reason = tables.Column("status_reason",
                                  verbose_name=_("Status Reason"))
    action = tables.Column("action", verbose_name=_("Action"))
    generated_at = tables.Column("generated_at",
                                 verbose_name=_("Generated At"),
                                 filters=(filters.parse_isotime,))

    class Meta(object):
        name = "event"
        verbose_name = _("Event")

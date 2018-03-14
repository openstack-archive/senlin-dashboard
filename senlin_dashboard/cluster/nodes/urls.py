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

from django.conf import settings
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from horizon.browsers import views
from senlin_dashboard.cluster.nodes import views as legacyView

if settings.ANGULAR_FEATURES.get('nodes_panel', True):
    title = _("Nodes")
    urlpatterns = [
        url('', views.AngularIndexView.as_view(title=title), name='index'),
    ]
else:
    urlpatterns = [
        url(r'^$', legacyView.IndexView.as_view(), name='index'),
        url(r'^create/$', legacyView.CreateView.as_view(), name='create'),
        url(r'^(?P<node_id>[^/]+)/$',
            legacyView.DetailView.as_view(), name='detail'),
        url(r'^(?P<node_id>[^/]+)/update/$',
            legacyView.UpdateView.as_view(), name='update'),
    ]

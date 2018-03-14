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

from horizon.browsers.views import AngularIndexView
from senlin_dashboard.cluster.profiles import views as legacyViews


if settings.ANGULAR_FEATURES.get('profiles_panel', True):
    title = _("Profiles")
    urlpatterns = [
        url(r'^(?P<profile_id>[^/]+)/$',
            legacyViews.DetailView.as_view(), name='detail'),
        url('', AngularIndexView.as_view(title=title), name='index'),
    ]
else:
    urlpatterns = [
        url(r'^$', legacyViews.IndexView.as_view(), name='index'),
        url(r'^create/$', legacyViews.CreateView.as_view(), name='create'),
        url(r'^(?P<profile_id>[^/]+)/update/$',
            legacyViews.UpdateView.as_view(), name='update'),
        url(r'^(?P<profile_id>[^/]+)/$',
            legacyViews.DetailView.as_view(), name='detail'),
    ]

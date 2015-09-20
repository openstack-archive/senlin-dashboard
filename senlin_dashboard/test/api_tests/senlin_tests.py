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

from senlinclient.v1 import models

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test


class SenlinApiTests(test.APITestCase):

    def test_cluster_list(self):
        clusters = self.clusters.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.list = self.mox.CreateMockAnything()
        senlinclient.list(models.Cluster).AndReturn(clusters)
        self.mox.ReplayAll()

        api.senlin.cluster_list(self.request)

    def test_profile_list(self):
        profiles = self.profiles.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.list = self.mox.CreateMockAnything()
        senlinclient.list(models.Profile).AndReturn(profiles)
        self.mox.ReplayAll()

        api.senlin.profile_list(self.request)

    def test_policy_list(self):
        policies = self.policies.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.list = self.mox.CreateMockAnything()
        senlinclient.list(models.Policy).AndReturn(policies)
        self.mox.ReplayAll()

        api.senlin.policy_list(self.request)

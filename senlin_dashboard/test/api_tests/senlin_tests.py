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

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test


class SenlinApiTests(test.APITestCase):

    def test_cluster_list(self):
        params = {}
        clusters = self.clusters.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.clusters = self.mox.CreateMockAnything()
        senlinclient.clusters(**params).AndReturn(clusters)
        self.mox.ReplayAll()

        api.senlin.cluster_list(self.request, params)

    def test_profile_list(self):
        params = {}
        profiles = self.profiles.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.profiles = self.mox.CreateMockAnything()
        senlinclient.profiles(**params).AndReturn(profiles)
        self.mox.ReplayAll()

        api.senlin.profile_list(self.request, params)

    def test_policy_list(self):
        params = {}
        policies = self.policies.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.policies = self.mox.CreateMockAnything()
        senlinclient.policies(**params).AndReturn(policies)
        self.mox.ReplayAll()

        api.senlin.policy_list(self.request, params)

    def test_node_list(self):
        params = {}
        nodes = self.nodes.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.nodes = self.mox.CreateMockAnything()
        senlinclient.nodes(**params).AndReturn(nodes)
        self.mox.ReplayAll()

        api.senlin.node_list(self.request, params)

    def test_event_list(self):
        params = {}
        events = self.events.list()
        senlinclient = self.stub_senlinclient()
        senlinclient.events = self.mox.CreateMockAnything()
        senlinclient.events(**params).AndReturn(events)
        self.mox.ReplayAll()

        api.senlin.event_list(self.request, params)

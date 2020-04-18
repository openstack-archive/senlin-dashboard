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

from unittest import mock

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test


class SenlinApiTests(test.APITestCase):

    def test_cluster_list(self):
        params = {'sort': 'created_at:desc',
                  'limit': 1000,
                  'marker': None}
        clusters = self.clusters.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.clusters = mock.Mock()
        senlinclient.clusters.return_value = clusters

        ret_val = api.senlin.cluster_list(self.request)
        for cluster in ret_val[0]:
            self.assertIsInstance(cluster, api.senlin.Cluster)

        senlinclient.clusters.assert_called_once_with(**params)

    def test_profile_list(self):
        params = {'sort': 'created_at:desc',
                  'limit': 1000,
                  'marker': None}
        profiles = self.profiles.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.profiles = mock.Mock()
        senlinclient.profiles.return_value = profiles

        ret_val = api.senlin.profile_list(self.request)
        for profile in ret_val[0]:
            self.assertIsInstance(profile, api.senlin.Profile)

        senlinclient.profiles.assert_called_once_with(**params)

    def test_policy_list(self):
        params = {'sort': 'created_at:desc',
                  'limit': 1000,
                  'marker': None}
        policies = self.policies.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.policies = mock.Mock()
        senlinclient.policies.return_value = policies

        ret_val, _more, _prev = api.senlin.policy_list(self.request)
        for policy in ret_val:
            self.assertIsInstance(policy, api.senlin.Policy)

        senlinclient.policies.assert_called_once_with(**params)

    def test_node_list(self):
        params = {'sort': 'name:desc',
                  'limit': 1000,
                  'marker': None,
                  'cluster_id': None}
        nodes = self.nodes.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.nodes = mock.Mock()
        senlinclient.nodes.return_value = nodes

        ret_val = api.senlin.node_list(self.request)
        for node in ret_val[0]:
            self.assertIsInstance(node, api.senlin.Node)

        senlinclient.nodes.assert_called_once_with(**params)

    def test_event_list(self):
        params = {'sort': 'timestamp:desc',
                  'limit': 1000,
                  'marker': None}
        events = self.events.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.events = mock.Mock()
        senlinclient.events.return_value = events

        ret_val = api.senlin.event_list(self.request)
        for event in ret_val[0]:
            self.assertIsInstance(event, api.senlin.Event)

        senlinclient.events.assert_called_once_with(**params)

    def test_receiver_list(self):
        params = {'sort': 'created_at:desc',
                  'limit': 1000,
                  'marker': None}
        receivers = self.receivers.list()
        senlinclient = self.stub_senlinclient()

        senlinclient.receivers = mock.Mock()
        senlinclient.receivers.return_value = receivers

        ret_val, _more, _prev = api.senlin.receiver_list(self.request)
        for receiver in ret_val:
            self.assertIsInstance(receiver, api.senlin.Receiver)

        senlinclient.receivers.assert_called_once_with(**params)

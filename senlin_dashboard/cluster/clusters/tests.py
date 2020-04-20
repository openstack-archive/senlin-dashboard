# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import mock

from django.urls import reverse

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

CLUSTER_INDEX_URL = reverse('horizon:cluster:clusters:index')
CLUSTER_CREATE_URL = reverse('horizon:cluster:clusters:create')
CLUSTER_DETAIL_URL = reverse(
    'horizon:cluster:clusters:detail',
    args=[u'123456'])
CLUSTER_MANAGE_POLICIES_URL = reverse(
    'horizon:cluster:clusters:manage_policies',
    args=[u'123456'])


class ClustersTest(test.TestCase):

    @test.create_mocks({api.senlin: ('cluster_list',)})
    def test_index(self):
        clusters = self.clusters.list()
        self.mock_cluster_list.return_value = \
            (clusters, False, False)

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertContains(res, '<h1>Clusters</h1>')
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertEqual(1, len(clusters))
        self.mock_cluster_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('cluster_list',)})
    def test_index_cluster_list_exception(self):
        self.mock_cluster_list.side_effect = \
            self.exceptions.senlin

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertEqual(0, len(res.context['clusters_table'].data))
        self.assertMessageCount(res, error=1)
        self.mock_cluster_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('cluster_list',)})
    def test_index_no_cluster(self):
        self.mock_cluster_list.return_value = \
            ([], False, False)

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(0, len(res.context['clusters_table'].data))
        self.mock_cluster_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('cluster_create',
                                     'profile_list',)})
    def test_create_node(self):
        profiles = self.profiles.list()

        formdata = {
            'name': 'test-cluster',
            'profile_id': '123456',
            'min_size': 0,
            'max_size': -1,
            'desired_capacity': 1,
            'parent': '',
            'timeout': 200,
            'metadata': ''
        }

        opts = formdata

        self.mock_profile_list.return_value = \
            (profiles, False, False)
        self.mock_cluster_create.return_value = opts

        res = self.client.post(CLUSTER_CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_mocks({api.senlin: ('cluster_get',
                                     'cluster_policy_list')})
    def test_cluster_detail(self):
        policies = self.policies.list()
        cluster = self.clusters.list()[0]
        self.mock_cluster_get.return_value = cluster
        self.mock_cluster_policy_list.return_value = policies

        res = self.client.get(CLUSTER_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-cluster')
        self.mock_cluster_get.assert_called_once_with(
            test.IsHttpRequest(), u'123456')
        self.mock_cluster_policy_list.assert_called_once_with(
            test.IsHttpRequest(), u'123456', {})

    @test.create_mocks({api.senlin: ('event_list',
                                     'cluster_get',
                                     'cluster_policy_list')})
    def test_cluster_event(self):
        cluster = self.clusters.list()[0]
        policies = self.policies.list()
        events = self.events.list()
        self.mock_cluster_get.return_value = cluster
        self.mock_event_list.return_value = events
        self.mock_cluster_policy_list.return_value = policies

        res = self.client.get(
            CLUSTER_DETAIL_URL + '?tab=cluster_details__event')
        self.assertTemplateUsed(res, 'cluster/nodes/_detail_event.html')
        self.assertContains(res, '123456')
        self.mock_cluster_get.assert_called_once_with(
            test.IsHttpRequest(), u'123456')
        self.mock_event_list.assert_called_once_with(
            test.IsHttpRequest(), filters={'obj_id': u'123456'},
            marker=None, paginate=True, reversed_order=False)
        self.mock_cluster_policy_list.assert_called_once_with(
            test.IsHttpRequest(), u'123456', {})

    @test.create_mocks({api.senlin: ('node_list',
                                     'cluster_get',
                                     'cluster_policy_list')})
    def test_cluster_nodes(self):
        policies = self.policies.list()
        cluster = self.clusters.list()[0]
        nodes = self.nodes.list()
        self.mock_cluster_get.return_value = cluster
        self.mock_node_list.return_value = nodes
        self.mock_cluster_policy_list.return_value = policies

        res = self.client.get(
            CLUSTER_DETAIL_URL + '?tab=cluster_details__nodes')
        self.assertTemplateUsed(res, 'cluster/clusters/_detail_nodes.html')
        self.assertContains(res, '123456')
        self.mock_cluster_get.assert_called_once_with(
            test.IsHttpRequest(), u'123456')
        self.mock_node_list.assert_called_once_with(
            test.IsHttpRequest(), cluster_id=u'123456')
        self.mock_cluster_policy_list.assert_called_once_with(
            test.IsHttpRequest(), u'123456', {})

    @test.create_mocks({api.senlin: ('policy_list',
                                     'cluster_policy_list')})
    def test_cluster_mamage_policies_index(self):
        policies = self.policies.list()
        cluster_policies = policies[:1]
        self.mock_policy_list.return_value = \
            [policies, False, False]
        self.mock_cluster_policy_list.side_effect = \
            [cluster_policies, cluster_policies]

        res = self.client.get(CLUSTER_MANAGE_POLICIES_URL)
        self.assertTemplateUsed(res, 'cluster/clusters/manage_policies.html')
        self.assertContains(res, 'test-policy02')
        self.mock_policy_list.assert_called_once_with(
            test.IsHttpRequest())
        self.mock_cluster_policy_list.assert_has_calls([
            mock.call(test.IsHttpRequest(), u'123456', {}),
            mock.call(test.IsHttpRequest(), u'123456', {})])

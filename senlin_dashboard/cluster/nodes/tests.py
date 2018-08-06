# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.urls import reverse

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

NODE_INDEX_URL = reverse('horizon:cluster:nodes:index')
NODE_CREATE_URL = reverse('horizon:cluster:nodes:create')
NODE_DETAIL_URL = reverse(
    'horizon:cluster:nodes:detail',
    args=[u'123456'])


class NodesTest(test.TestCase):

    @test.create_mocks({api.senlin: ('node_list',)})
    def test_index(self):
        nodes = self.nodes.list()
        self.mock_node_list.return_value = nodes

        res = self.client.get(NODE_INDEX_URL)
        self.assertContains(res, '<h1>Nodes</h1>')
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(1, len(nodes))
        self.mock_node_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('node_list',)})
    def test_index_node_list_exception(self):
        self.mock_node_list.side_effect = self.exceptions.senlin

        res = self.client.get(NODE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(0, len(res.context['nodes_table'].data))
        self.mock_node_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('node_list',)})
    def test_index_no_node(self):
        self.mock_node_list.return_value = []

        res = self.client.get(NODE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(0, len(res.context['nodes_table'].data))
        self.mock_node_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('node_create',
                                     'profile_list',
                                     'cluster_list')})
    def test_create_node(self):
        profiles = self.profiles.list()
        clusters = self.clusters.list()

        formdata = {
            'name': 'test-node',
            'profile_id': '123456',
            'cluster_id': '',
            'role': '',
            'metadata': ''
        }

        self.mock_profile_list.return_value = \
            (profiles, False, False)
        self.mock_cluster_list.return_value = \
            (clusters, False, False)
        self.mock_node_create.return_value = formdata

        res = self.client.post(NODE_CREATE_URL, formdata)
        self.assertNoFormErrors(res)
        self.mock_profile_list.assert_called_once_with(
            test.IsHttpRequest())
        self.mock_cluster_list.assert_called_once_with(
            test.IsHttpRequest())

    @test.create_mocks({api.senlin: ('node_get',)})
    def test_node_detail(self):
        node = self.nodes.list()[0]
        self.mock_node_get.return_value = node

        res = self.client.get(NODE_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-node')
        self.mock_node_get.assert_called_once_with(
            test.IsHttpRequest(), u'123456')

    @test.create_mocks({api.senlin: ('event_list',
                                     'node_get')})
    def test_node_event(self):
        events = self.events.list()
        node = self.nodes.list()[0]
        self.mock_node_get.return_value = node
        self.mock_event_list.return_value = events

        res = self.client.get(NODE_DETAIL_URL + '?tab=node_details__event')
        self.assertTemplateUsed(res, 'cluster/nodes/_detail_event.html')
        self.assertContains(res, '123456')
        self.mock_node_get.assert_called_once_with(
            test.IsHttpRequest(), u'123456')
        self.mock_event_list.assert_called_once_with(
            test.IsHttpRequest(), filters={'obj_id': u'123456'},
            marker=None, paginate=True, reversed_order=False)

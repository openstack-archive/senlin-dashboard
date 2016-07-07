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

from django.core.urlresolvers import reverse_lazy
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

NODE_INDEX_URL = reverse_lazy('horizon:cluster:nodes:index')
NODE_CREATE_URL = reverse_lazy('horizon:cluster:nodes:create')
NODE_DETAIL_URL = reverse_lazy(
    'horizon:cluster:nodes:detail',
    args=[u'123456'])


class NodesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index(self):
        nodes = self.nodes.list()
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndReturn(nodes)
        self.mox.ReplayAll()

        res = self.client.get(NODE_INDEX_URL)
        self.assertContains(res, '<h1>Nodes</h1>')
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(len(nodes), 1)

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index_node_list_exception(self):
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(NODE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(len(res.context['nodes_table'].data), 0)

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index_no_node(self):
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(NODE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['nodes_table'].data), 0)

    @test.create_stubs({api.senlin: ('node_create',
                                     'profile_list',
                                     'cluster_list')})
    def test_create_node(self):
        node = self.nodes.list()[0]
        profiles = self.profiles.list()
        clusters = self.clusters.list()

        formdata = {
            'name': 'test-node',
            'profile_id': '123456',
            'cluster_id': '',
            'role': '',
            'metadata': ''
        }

        opts = formdata

        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn(profiles)
        api.senlin.cluster_list(
            IsA(http.HttpRequest)).AndReturn(clusters)
        api.senlin.node_create(
            IsA(http.HttpRequest), opts).AndReturn(node)
        self.mox.ReplayAll()

        res = self.client.post(NODE_CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_stubs({api.senlin: ('node_get',)})
    def test_node_detail(self):
        node = self.nodes.list()[0]
        api.senlin.node_get(
            IsA(http.HttpRequest), u'123456').AndReturn(node)
        self.mox.ReplayAll()

        res = self.client.get(NODE_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-node')

    @test.create_stubs({api.senlin: ('event_list',
                                     'node_get')})
    def test_node_event(self):
        events = self.events.list()
        node = self.nodes.list()[0]
        api.senlin.node_get(
            IsA(http.HttpRequest), u'123456').AndReturn(node)
        api.senlin.event_list(
            IsA(http.HttpRequest),
            params={'obj_id': u'123456'}).AndReturn(events)
        self.mox.ReplayAll()

        res = self.client.get(NODE_DETAIL_URL + '?tab=node_details__event')
        self.assertTemplateUsed(res, 'cluster/nodes/_detail_event.html')
        self.assertContains(res, '123456')

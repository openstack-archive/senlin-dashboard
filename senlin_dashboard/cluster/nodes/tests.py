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

from django.core.urlresolvers import reverse
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse('horizon:cluster:nodes:index')


class NodesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index(self):
        nodes = self.nodes.list()
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndReturn(nodes)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(len(nodes), 1)

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index_node_list_exception(self):
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertEqual(len(res.context['nodes_table'].data), 0)

    @test.create_stubs({api.senlin: ('node_list',)})
    def test_index_no_node(self):
        api.senlin.node_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/nodes/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['nodes_table'].data), 0)

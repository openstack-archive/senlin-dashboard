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

from django.core.urlresolvers import reverse
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

CLUSTER_INDEX_URL = reverse('horizon:cluster:clusters:index')
CLUSTER_CREATE_URL = reverse('horizon:cluster:clusters:create')
CLUSTER_DETAIL_URL = reverse('horizon:cluster:clusters:detail',
                             args=[u'123456'])


class ClustersTest(test.TestCase):

    @test.create_stubs({api.senlin: ('cluster_list',)})
    def test_index(self):
        clusters = self.clusters.list()
        api.senlin.cluster_list(
            IsA(http.HttpRequest), params={}).AndReturn(clusters)
        self.mox.ReplayAll()

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertContains(res, '<h1>Clusters</h1>')
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertEqual(len(clusters), 1)

    @test.create_stubs({api.senlin: ('cluster_list',)})
    def test_index_cluster_list_exception(self):
        api.senlin.cluster_list(
            IsA(http.HttpRequest), params={}).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertEqual(len(res.context['clusters_table'].data), 0)
        self.assertMessageCount(res, error=1)

    @test.create_stubs({api.senlin: ('cluster_list',)})
    def test_index_no_cluster(self):
        api.senlin.cluster_list(
            IsA(http.HttpRequest), params={}).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(CLUSTER_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/clusters/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['clusters_table'].data), 0)

    @test.create_stubs({api.senlin: ('cluster_create',
                                     'profile_list',)})
    def test_create_node(self):
        cluster = self.clusters.list()[0]
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

        api.senlin.profile_list(
            IsA(http.HttpRequest), params={}).AndReturn(profiles)
        api.senlin.cluster_create(
            IsA(http.HttpRequest), opts).AndReturn(cluster)
        self.mox.ReplayAll()

        res = self.client.post(CLUSTER_CREATE_URL, formdata)
        self.assertNoFormErrors(res)
        self.assertRedirectsNoFollow(res, CLUSTER_INDEX_URL)

    @test.create_stubs({api.senlin: ('cluster_get',)})
    def test_cluster_detail(self):
        cluster = self.clusters.list()[0]
        api.senlin.cluster_get(
            IsA(http.HttpRequest), u'123456').AndReturn(cluster)
        self.mox.ReplayAll()

        res = self.client.get(CLUSTER_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-cluster')

    @test.create_stubs({api.senlin: ('event_list',
                                     'cluster_get')})
    def test_cluster_event(self):
        events = self.events.list()
        node = self.nodes.list()[0]
        api.senlin.cluster_get(
            IsA(http.HttpRequest), u'123456').AndReturn(node)
        api.senlin.event_list(
            IsA(http.HttpRequest),
            params={'obj_id': u'123456'}).AndReturn(events)
        self.mox.ReplayAll()

        res = self.client.get(
            CLUSTER_DETAIL_URL + '?tab=cluster_details__event')
        self.assertTemplateUsed(res, 'cluster/nodes/_detail_event.html')
        self.assertContains(res, '123456')

    @test.create_stubs({api.senlin: ('node_list',
                                     'cluster_get')})
    def test_cluster_nodes(self):
        cluster = self.clusters.list()[0]
        nodes = self.nodes.list()
        api.senlin.cluster_get(
            IsA(http.HttpRequest), u'123456').AndReturn(cluster)
        api.senlin.node_list(
            IsA(http.HttpRequest),
            params={'cluster_id': u'123456'}).AndReturn(nodes)
        self.mox.ReplayAll()

        res = self.client.get(
            CLUSTER_DETAIL_URL + '?tab=cluster_details__nodes')
        self.assertTemplateUsed(res, 'cluster/clusters/_detail_nodes.html')
        self.assertContains(res, '123456')

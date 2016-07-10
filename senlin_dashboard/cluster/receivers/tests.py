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

from django.core.urlresolvers import reverse_lazy
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse_lazy('horizon:cluster:receivers:index')
CREATE_URL = reverse_lazy('horizon:cluster:receivers:create')


class ReceiversTest(test.TestCase):

    @test.create_stubs({api.senlin: ('receiver_list',)})
    def test_index(self):
        receivers = self.receivers.list()
        api.senlin.receiver_list(
            IsA(http.HttpRequest)).AndReturn(receivers)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertContains(res, '<h1>Receivers</h1>')
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertEqual(len(receivers), 1)

    @test.create_stubs({api.senlin: ('receiver_list',)})
    def test_index_receiver_list_exception(self):
        api.senlin.receiver_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertEqual(len(res.context['receivers_table'].data), 0)
        self.assertMessageCount(res, error=1)

    @test.create_stubs({api.senlin: ('receiver_list',)})
    def test_index_no_receiver(self):
        api.senlin.receiver_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['receivers_table'].data), 0)

    @test.create_stubs({api.senlin: ('receiver_create',
                                     'cluster_list')})
    def test_create_receiver(self):
        clusters = self.clusters.list()
        receiver = self.receivers.list()[0]
        data = {
            'name': 'test-receiver',
            'type': 'webhook',
            'cluster_id': '123456',
            'action': 'CLUSTER_SCALE_IN',
            'params': ''
        }

        api.senlin.cluster_list(
            IsA(http.HttpRequest)).AndReturn(clusters)
        api.senlin.receiver_create(
            IsA(http.HttpRequest), data).AndReturn(receiver)
        self.mox.ReplayAll()

        res = self.client.post(CREATE_URL, data)
        self.assertNoFormErrors(res)

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

from django.urls import reverse

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse('horizon:cluster:receivers:index')
CREATE_URL = reverse('horizon:cluster:receivers:create')


class ReceiversTest(test.TestCase):

    @test.create_mocks({api.senlin: ('receiver_list',)})
    def test_index(self):
        receivers = self.receivers.list()
        self.mock_receiver_list.return_value = receivers

        res = self.client.get(INDEX_URL)
        self.assertContains(res, '<h1>Receivers</h1>')
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertEqual(1, len(receivers))
        self.mock_receiver_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('receiver_list',)})
    def test_index_receiver_list_exception(self):
        self.mock_receiver_list.side_effect = (
            self.exceptions.senlin)

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertEqual(0, len(res.context['receivers_table'].data))
        self.assertMessageCount(res, error=1)
        self.mock_receiver_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('receiver_list',)})
    def test_index_no_receiver(self):
        self.mock_receiver_list.return_value = []

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/receivers/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(0, len(res.context['receivers_table'].data))
        self.mock_receiver_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('receiver_create',
                                     'cluster_list')})
    def test_create_receiver(self):
        clusters = self.clusters.list()
        data = {
            'name': 'test-receiver',
            'type': 'webhook',
            'cluster_id': '123456',
            'action': 'CLUSTER_SCALE_IN',
            'params': ''
        }
        formdata = {
            'name': 'test-receiver',
            'type': 'webhook',
            'cluster_id': '123456',
            'action': 'CLUSTER_SCALE_IN',
            'params': ''
        }

        self.mock_cluster_list.return_value = (
            (clusters, False, False))
        self.mock_receiver_create.return_value = data

        res = self.client.post(CREATE_URL, formdata)
        self.assertNoFormErrors(res)

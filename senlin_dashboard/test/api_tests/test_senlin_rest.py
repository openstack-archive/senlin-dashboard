# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from openstack_dashboard.test import helpers as test

from senlin_dashboard.api.rest import senlin


class SenlinRestTestCase(test.TestCase):

    #
    # Receiver
    #

    _receivers = [
        {
            'id': '1',
            'name': 'test-receiver1',
            'type': 'webhook',
            'cluster_id': 'c1',
            'action': 'CLUSTER_SCALE_OUT',
            'params': None,
            'channel': None
        },
        {
            'id': '2',
            'name': 'test-receiver2',
            'type': 'message',
            'cluster_id': None,
            'action': None,
            'params': None,
            'channel': None
        },
    ]

    @mock.patch.object(senlin, 'senlin')
    def test_receivers_get(self, client):
        request = self.mock_rest_request(**{'GET': {}})
        client.receiver_list.return_value = ([
            mock.Mock(**{'to_dict.return_value': self._receivers[0]}),
            mock.Mock(**{'to_dict.return_value': self._receivers[1]}),
        ], False, True)

        response = senlin.Receivers().get(request)
        self.assertStatusCode(response, 200)
        self.assertEqual(2, len(response.json['items']))
        self.assertFalse(response.json['has_more_data'])
        self.assertTrue(response.json['has_prev_data'])

    @mock.patch.object(senlin, 'senlin')
    def test_receiver_get_single(self, client):
        request = self.mock_rest_request()
        client.receiver_get.return_value.to_dict.return_value = \
            self._receivers[0]

        response = senlin.Receiver().get(request, '1')
        self.assertStatusCode(response, 200)
        self.assertEqual('test-receiver1', response.json['name'])

    @mock.patch.object(senlin, 'senlin')
    def test_receiver_delete(self, client):
        request = self.mock_rest_request()
        senlin.Receiver().delete(request, '1')
        client.receiver_delete.assert_called_once_with(request, '1')

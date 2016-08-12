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

import mock

from openstack_dashboard.test import helpers as test
from senlin_dashboard.api.rest import senlin


class SenlinRestTestCase(test.TestCase):

    #
    # Receiver
    #

    @mock.patch.object(senlin, 'senlin')
    def test_receivers_get(self, client):
        request = self.mock_rest_request(**{'GET': {}})
        client.receiver_list.return_value = ([
            mock.Mock(**{'to_dict.return_value': {'id': 'one'}}),
            mock.Mock(**{'to_dict.return_value': {'id': 'two'}}),
        ], False, True)

        response = senlin.Receivers().get(request)
        self.assertStatusCode(response, 200)
        self.assertEqual(len(response.json['items']), 2)
        self.assertEqual(response.json['has_more_data'], False)
        self.assertEqual(response.json['has_prev_data'], True)

    @mock.patch.object(senlin, 'senlin')
    def test_receiver_get_single(self, client):
        request = self.mock_rest_request()
        client.receiver_get.return_value.to_dict.return_value = {
            'name': 'test-receiver'}

        response = senlin.Receiver().get(request, '1')
        self.assertStatusCode(response, 200)
        self.assertEqual(response.json['name'], 'test-receiver')

    @mock.patch.object(senlin, 'senlin')
    def test_receiver_delete(self, client):
        request = self.mock_rest_request()
        senlin.Receiver().delete(request, "1")
        client.receiver_delete.assert_called_once_with(request, "1")

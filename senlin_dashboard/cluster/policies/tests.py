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

import yaml

from django.urls import reverse

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse('horizon:cluster:policies:index')
CREATE_URL = reverse('horizon:cluster:policies:create')
DETAIL_URL = reverse('horizon:cluster:policies:detail', args=[u'1'])


class PoliciesTest(test.TestCase):

    @test.create_mocks({api.senlin: ('policy_list',)})
    def test_index(self):
        policies = self.policies.list()
        self.mock_policy_list.return_value = policies

        res = self.client.get(INDEX_URL)
        self.assertContains(res, '<h1>Policies</h1>')
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertEqual(2, len(policies))
        self.mock_policy_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('policy_list',)})
    def test_index_policy_list_exception(self):
        self.mock_policy_list.side_effect = (
            self.exceptions.senlin)

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertEqual(0, len(res.context['policies_table'].data))
        self.assertMessageCount(res, error=1)
        self.mock_policy_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('policy_list',)})
    def test_index_no_policy(self):
        self.mock_policy_list.return_value = []

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(0, len(res.context['policies_table'].data))
        self.mock_policy_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('policy_create',)})
    def test_create_policy(self):
        spec_yaml = """
        type: senlin.policy.deletion
        version: 1.0
        description: A policy.
        properties:
          criteria: OLDEST_FIRST
          destroy_after_deletion: True
          grace_period: 60
          reduce_desired_capacity: False
        """

        formdata = {
            'name': 'test-policy',
            'spec': yaml.safe_load(spec_yaml),
            'cooldown': 0,
            'level': 0
        }

        args = {
            'name': 'test-policy',
            'spec': yaml.safe_load(spec_yaml),
            'cooldown': 0,
            'level': 0
        }

        self.mock_policy_create.return_value = args

        res = self.client.post(CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_mocks({api.senlin: ('policy_get',)})
    def test_policy_detail(self):
        policy = self.policies.list()[0]
        self.mock_policy_get.return_value = policy

        res = self.client.get(DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-policy')
        self.mock_policy_get.assert_called_once_with(
            test.IsHttpRequest(), u'1')

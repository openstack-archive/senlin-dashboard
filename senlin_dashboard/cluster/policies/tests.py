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

from django.core.urlresolvers import reverse_lazy
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse_lazy('horizon:cluster:policies:index')
CREATE_URL = reverse_lazy('horizon:cluster:policies:create')
DETAIL_URL = reverse_lazy('horizon:cluster:policies:detail', args=[u'1'])


class PoliciesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('policy_list',)})
    def test_index(self):
        policies = self.policies.list()
        api.senlin.policy_list(
            IsA(http.HttpRequest)).AndReturn(policies)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertContains(res, '<h1>Policies</h1>')
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertEqual(len(policies), 2)

    @test.create_stubs({api.senlin: ('policy_list',)})
    def test_index_policy_list_exception(self):
        api.senlin.policy_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertEqual(len(res.context['policies_table'].data), 0)
        self.assertMessageCount(res, error=1)

    @test.create_stubs({api.senlin: ('policy_list',)})
    def test_index_no_policy(self):
        api.senlin.policy_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['policies_table'].data), 0)

    @test.create_stubs({api.senlin: ('policy_create',)})
    def test_create_policy(self):
        policy = self.policies.list()[0]

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
            'spec': yaml.load(spec_yaml),
            'cooldown': 0,
            'level': 0
        }

        args = {
            'name': 'test-policy',
            'spec': yaml.load(spec_yaml),
            'cooldown': 0,
            'level': 0
        }

        api.senlin.policy_create(
            IsA(http.HttpRequest), args).AndReturn(policy)
        self.mox.ReplayAll()

        res = self.client.post(CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_stubs({api.senlin: ('policy_get',)})
    def test_policy_detail(self):
        policy = self.policies.list()[0]
        api.senlin.policy_get(
            IsA(http.HttpRequest), u'1').AndReturn(policy)
        self.mox.ReplayAll()

        res = self.client.get(DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-policy')

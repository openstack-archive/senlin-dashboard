# Copyright 2015 99Cloud Technologies Co., Ltd.
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

INDEX_URL = reverse('horizon:cluster:policies:index')


class PoliciesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('policy_list',)})
    def test_index(self):
        policies = self.policies.list()
        api.senlin.policy_list(
            IsA(http.HttpRequest)).AndReturn(policies)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/policies/index.html')
        self.assertEqual(len(policies), 1)

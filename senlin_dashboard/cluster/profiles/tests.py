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

from django.urls import reverse

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

PROFILE_INDEX_URL = reverse('horizon:cluster:profiles:index')
PROFILE_CREATE_URL = reverse('horizon:cluster:profiles:create')
PROFILE_DETAIL_URL = reverse(
    'horizon:cluster:profiles:detail', args=[u'1'])


class ProfilesTest(test.TestCase):

    @test.create_mocks({api.senlin: ('profile_list',)})
    def test_index(self):
        profiles = self.profiles.list()
        """
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn(profiles)
        self.mox.ReplayAll()
        """
        self.mock_profile_list.return_value = profiles

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertContains(res, '<h1>Profiles</h1>')
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(1, len(profiles))
        self.mock_profile_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None, paginate=True,
            reversed_order=False)

    @test.create_mocks({api.senlin: ('profile_list',)})
    def test_index_profile_list_exception(self):
        self.mock_profile_list.side_effect = self.exceptions.senlin

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(0, len(res.context['profiles_table'].data))
        self.mock_profile_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None, paginate=True,
            reversed_order=False)

    @test.create_mocks({api.senlin: ('profile_list',)})
    def test_index_no_policy(self):
        self.mock_profile_list.return_value = []

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(0, len(res.context['profiles_table'].data))
        self.mock_profile_list.assert_called_once_with(
            test.IsHttpRequest(), filters={}, marker=None,
            paginate=True, reversed_order=False)

    @test.create_mocks({api.senlin: ('profile_create',)})
    def test_create_profile(self):
        spec_yaml = \
            'type: os.nova.server\n'\
            'version: 1.0\n'\
            'properties:\n'\
            '  name: cirros_server\n'\
            '  flavor: 1\n'\
            '  image: "cirros-0.3.4-x86_64-uec"\n'\
            '  key_name: oskey\n'\
            '  networks:\n'\
            '    - network: private\n'

        formdata = {
            'name': 'test-profile',
            'source_type': 'yaml',
            'spec_yaml': spec_yaml,
            'metadata': ''
        }

        opts = {
            'name': 'test-profile',
            'spec_yaml': spec_yaml,
            'type': 'os.nova.server',
            'metadata': None
        }

        self.mock_profile_create.return_value = opts

        res = self.client.post(PROFILE_CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_mocks({api.senlin: ('profile_get',)})
    def test_profile_detail(self):
        profile = self.profiles.list()[0]
        self.mock_profile_get.return_value = profile

        res = self.client.get(PROFILE_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-profile')
        self.mock_profile_get.assert_called_once_with(
            test.IsHttpRequest(), u'1')

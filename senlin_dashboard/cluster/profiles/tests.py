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

from django.core.urlresolvers import reverse_lazy
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

PROFILE_INDEX_URL = reverse_lazy('horizon:cluster:profiles:index')
PROFILE_CREATE_URL = reverse_lazy('horizon:cluster:profiles:create')
PROFILE_DETAIL_URL = reverse_lazy(
    'horizon:cluster:profiles:detail', args=[u'1'])


class ProfilesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index(self):
        profiles = self.profiles.list()
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn(profiles)
        self.mox.ReplayAll()

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertContains(res, '<h1>Profiles</h1>')
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(len(profiles), 1)

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index_profile_list_exception(self):
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(len(res.context['profiles_table'].data), 0)

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index_no_policy(self):
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(PROFILE_INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['profiles_table'].data), 0)

    @test.create_stubs({api.senlin: ('profile_create',)})
    def test_create_profile(self):
        profile = self.profiles.list()[0]

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
            'metadata': None
        }

        opts = {
            'name': 'test-profile',
            'spec_yaml': spec_yaml,
            'type': 'os.nova.server',
            'metadata': None
        }

        api.senlin.profile_create(
            IsA(http.HttpRequest), opts).AndReturn(profile)
        self.mox.ReplayAll()

        res = self.client.post(PROFILE_CREATE_URL, formdata)
        self.assertNoFormErrors(res)

    @test.create_stubs({api.senlin: ('profile_get',)})
    def test_profile_detail(self):
        profile = self.profiles.list()[0]
        api.senlin.profile_get(
            IsA(http.HttpRequest), u'1').AndReturn(profile)
        self.mox.ReplayAll()

        res = self.client.get(PROFILE_DETAIL_URL)
        self.assertTemplateUsed(res, 'horizon/common/_detail.html')
        self.assertContains(res, 'test-profile')

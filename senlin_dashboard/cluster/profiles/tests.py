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

import json

from django.core.urlresolvers import reverse
from django import http

from mox3.mox import IsA  # noqa

from senlin_dashboard import api
from senlin_dashboard.test import helpers as test

INDEX_URL = reverse('horizon:cluster:profiles:index')


class ProfilesTest(test.TestCase):

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index(self):
        profiles = self.profiles.list()
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn(profiles)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(len(profiles), 1)

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index_profile_list_exception(self):
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndRaise(self.exceptions.senlin)
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertEqual(len(res.context['profiles_table'].data), 0)

    @test.create_stubs({api.senlin: ('profile_list',)})
    def test_index_no_policy(self):
        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn([])
        self.mox.ReplayAll()

        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, 'cluster/profiles/index.html')
        self.assertContains(res, 'No items to display')
        self.assertEqual(len(res.context['profiles_table'].data), 0)

    @test.create_stubs({api.senlin: ('profile_list',
                                     'profile_create',
                                     'profile_type_list')})
    def test_create_profile(self):
        profiles = self.policies.list()
        profile = profiles[0]
        profile_type = self.profile_types.list()[0]

        spec = {'properties':
                {'name': 'nova_instance',
                 'flavor': 2,
                 'image': 'cirros-0.3.4-x86_64-uec',
                 'key_name': 'test_key'},
                'type': 'os.nova.server',
                'version': 1.0}
        post_data = {"name": "Profile1",
                     "prof_type": profile_type.name,
                     "spec": json.dumps(spec)}
        formData = api.senlin._profile_dict(
            name=post_data['name'],
            prof_type=post_data['prof_type'],
            spec=post_data['spec'],
            permission='',
            metadata=None)

        api.senlin.profile_list(
            IsA(http.HttpRequest)).AndReturn(profiles)
        api.senlin.profile_type_list(IsA(http.HttpRequest)).\
            AndReturn(self.profile_types.list())
        api.senlin.profile_create(IsA(http.HttpRequest), formData).\
            AndReturn(profile)
        self.mox.ReplayAll()

        url = reverse('horizon:cluster:profiles:create')
        res = self.client.post(url, post_data)
        self.assertNoFormErrors(res)

        redirect_url = reverse('horizon:cluster:profiles:index')
        self.assertRedirectsNoFollow(res, redirect_url)

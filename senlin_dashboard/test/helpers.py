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

from openstack_dashboard.test import helpers

from senlinclient import client as senlin_client

from senlin_dashboard import api
from senlin_dashboard.test.test_data import utils


def create_stubs(stubs_to_create={}):
    return helpers.create_stubs(stubs_to_create)


class SenlinTestsMixin(object):
    def _setup_test_data(self):
        super(SenlinTestsMixin, self)._setup_test_data()
        utils.load_test_data(self)


class TestCase(SenlinTestsMixin, helpers.TestCase):
    pass


class APITestCase(SenlinTestsMixin, helpers.APITestCase):
    def setUp(self):
        super(APITestCase, self).setUp()

        # Store the original senlin client
        self._original_senlinclient = api.senlin.senlinclient

        # Replace the clients with our stubs.
        api.senlin.senlinclient = lambda request: self.stub_senlinclient()

    def tearDown(self):
        super(APITestCase, self).tearDown()
        api.senlin.senlinclient = self._original_senlinclient

    def stub_senlinclient(self):
        if not hasattr(self, "senlinclient"):
            self.mox.StubOutWithMock(senlin_client, 'Client')
            self.senlinclient = self.mox.CreateMock(senlin_client.Client)
        return self.senlinclient

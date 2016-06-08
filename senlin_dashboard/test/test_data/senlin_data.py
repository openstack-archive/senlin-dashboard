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

import mock

from openstack_dashboard.test.test_data import utils as test_data_utils


def data(TEST):
    # Profiles
    TEST.profiles = test_data_utils.TestDataContainer()
    profile_1 = mock.Mock()
    profile_1.id = "123456"
    profile_1.name = "test-profile"
    profile_1.metadata = {}
    profile_1.spec = {
        'type': 'os.nova.server',
        'version': '1.0',
        'properties': {
            'name': 'cirros_server',
            'flavor': 1,
            'image': 'cirros-0.3.4-x86_64-uec',
            'key_name': 'oskey',
            'networks': [{'network': 'private'}]
        },
    }

    TEST.profiles.add(profile_1)

    # Profile types
    TEST.profile_types = test_data_utils.TestDataContainer()
    profile_type_1 = mock.Mock()
    profile_type_1.name = "test-profile-type"

    TEST.profile_types.add(profile_type_1)

    # Clusters
    TEST.clusters = test_data_utils.TestDataContainer()
    cluster_1 = mock.Mock()
    cluster_1.id = "123456"
    cluster_1.name = "test-cluster"

    TEST.clusters.add(cluster_1)

    # Policies
    TEST.policies = test_data_utils.TestDataContainer()
    policy_1 = mock.Mock()
    policy_1.id = "123"
    policy_1.name = "test-policy01"
    policy_1.spec = {}
    policy_2 = mock.Mock()
    policy_1.id = "456"
    policy_2.name = "test-policy02"
    policy_2.spec = {}

    TEST.policies.add(policy_1)
    TEST.policies.add(policy_2)

    # Nodes
    TEST.nodes = test_data_utils.TestDataContainer()
    node_1 = mock.Mock()
    node_1.id = "123456"
    node_1.name = "test-node"

    TEST.nodes.add(node_1)

    # Events
    TEST.events = test_data_utils.TestDataContainer()
    event_1 = mock.Mock()
    event_1.name = "test-event"

    TEST.events.add(event_1)

    # Receivers
    TEST.receivers = test_data_utils.TestDataContainer()
    receiver_1 = mock.Mock()
    receiver_1.name = "test-receiver"

    TEST.receivers.add(receiver_1)

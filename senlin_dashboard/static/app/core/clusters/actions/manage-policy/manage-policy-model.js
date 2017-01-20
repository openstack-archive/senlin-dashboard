/**
 * Copyright 2016 NEC Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.manage-policy.model', managePolicyModel);

  managePolicyModel.$inject = [
    '$q',
    'horizon.app.core.openstack-service-api.senlin'
  ];

  function managePolicyModel($q, senlin) {
    var model = {
      id: "",
      policies: [],
      newSpec: {
        policies: []
      },
      updateAttachPolicy: updateAttachPolicy
    };

    function updateAttachPolicy() {
      var policyIds = [];
      var newAttachPolicies = model.newSpec.policies;
      for (var i = 0; i < newAttachPolicies.length; i++) {
        policyIds.push(newAttachPolicies[i].id);
      }

      return senlin.updateClusterPolicies(model.id, {ids: policyIds}, true);
    }

    return model;
  }
})();

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

  /**
   * @ngdoc factory
   * @name horizon.cluster.clusters.actions.manage-policy.service
   * @description
   * Service for updating policies for the cluster
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .factory('horizon.cluster.clusters.actions.manage-policy.service', managePolicyService);

  managePolicyService.$inject = [
    '$q',
    '$location',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.modal.wizard-modal.service',
    'horizon.framework.widgets.toast.service',
    'horizon.app.core.clusters.resourceType',
    'horizon.cluster.clusters.actions.manage-policy.service.workflow',
    'horizon.cluster.clusters.actions.manage-policy.model',
    'horizon.app.core.openstack-service-api.senlin'
  ];

  function managePolicyService(
    $q,
    $location,
    policy,
    actionResult,
    gettext,
    $qExtensions,
    wizardModalService,
    toast,
    resourceType,
    managePolicyWorkflow,
    model,
    senlin
  ) {

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function perform(selected) {
      model.id = selected.id;
      $q.all([
        senlin.getPolicies(),
        senlin.getClusterPolicies(selected.id)
      ]).then(onLoad);
    }

    function onLoad(response) {
      var allPolicies = response[0].data.items;
      var policiesOnCluster = modifyResponse(response[1].data.items);

      function modifyResponse(items) {
        return items.map(modifyItem);

        // the format of return values of cluster_policy_list is different
        // with the one of policy_list.
        function modifyItem(item) {
          item.name = item.policy_name;
          item.type = item.policy_type;
          item.id = item.policy_id;
          return item;
        }
      }

      model.policies = allPolicies;
      model.newSpec = { policies: policiesOnCluster };

      return wizardModalService.modal({
        workflow: managePolicyWorkflow,
        submit: submit,
        data: model
      }).result;
    }

    function submit() {
      return model.updateAttachPolicy().then(success);
    }

    function success(response) {
      toast.add('success', gettext('Policies on the cluster were successfully updated.'));
      var result = actionResult.getActionResult()
                   .created(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.created.length > 0) {
        $location.path("/cluster");
      } else {
        return result.result;
      }
    }
  }
})();

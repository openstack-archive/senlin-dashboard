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
   * @name horizon.cluster.profiles.actions.update.service
   * @description
   * Service for the cluster profile update modal
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .factory('horizon.cluster.profiles.actions.update.service', updateService);

  updateService.$inject = [
    '$location',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.profiles.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.modal.wizard-modal.service',
    'horizon.framework.widgets.toast.service',
    'horizon.cluster.profiles.actions.create.model',
    'horizon.cluster.profiles.actions.update.service.workflow'
  ];

  function updateService(
    $location, policy, senlin, resourceType, actionResult, gettext, $qExtensions,
    wizardModalService, toast, model, updateWorkflow
  ) {

    var message = {
      success: gettext('Profile %s was successfully updated.')
    };

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function perform(selected, scope) {
      scope.model = model;
      scope.model.init('update', selected.id);

      return wizardModalService.modal({
        scope: scope,
        workflow: updateWorkflow,
        submit: submit,
        data: scope.model
      }).result;
    }

    function allowed() {
      return policy.ifAllowed({ rules: [['cluster', 'profiles:update']] });
    }

    function submit() {
      return model.setProfile().then(success, true);
    }

    function success(response) {
      toast.add('success', interpolate(message.success, [response.data.id]));
      var result = actionResult.getActionResult()
                   .updated(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.updated.length > 0) {
        $location.path("/cluster/profiles");
      } else {
        return result.result;
      }
    }
  }
})();

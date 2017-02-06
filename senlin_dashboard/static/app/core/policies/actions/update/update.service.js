/**
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
   * @name horizon.cluster.policies.actions.create.service
   * @description
   * Service for the cluster policy create modal
   */
  angular
    .module('horizon.cluster.policies.actions')
    .factory('horizon.cluster.policies.actions.update.service', updateService);

  updateService.$inject = [
    '$location',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.policies.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service',
    'horizon.cluster.policies.actions.workflow'
  ];

  function updateService(
    $location, policy, senlin, resourceType, actionResult, gettext,
    $qExtensions, modal, toast, workflow
  ) {

    var message = {
      success: gettext('Policy %s was successfully updated.')
    };

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function perform(selected, scope) {
      // modal title, buttons
      var title, submitText;
      title = gettext('Update Policy');
      submitText = gettext('Update');

      var config = workflow.init('update', title, submitText, scope);

      // load current data
      senlin.getPolicy(selected.id).then(onLoad);
      function onLoad(response) {
        config.model.id = response.data.id;
        config.model.name = response.data.name;
        config.model.spec = response.data.spec;
      }

      return modal.open(config).then(submit);
    }

    function allowed() {
      return policy.ifAllowed({ rules: [['cluster', 'policies:update']] });
    }

    function submit(context) {
      var id = context.model.id;
      delete context.model.id;
      delete context.model.spec;
      return senlin.updatePolicy(id, context.model, false).then(success, true);
    }

    function success(response) {
      toast.add('success', interpolate(message.success, [response.data.name]));
      var result = actionResult.getActionResult()
                   .updated(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.updated.length > 0) {
        $location.path("/cluster/policies");
      } else {
        return result.result;
      }
    }
  }
})();

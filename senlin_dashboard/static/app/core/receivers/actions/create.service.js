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
   * @name horizon.cluster.receivers.actions.create.service
   * @description
   * Service for the cluster receiver create modal
   */
  angular
    .module('horizon.cluster.receivers.actions')
    .factory('horizon.cluster.receivers.actions.create.service', createService);

  createService.$inject = [
    '$location',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.receivers.basePath',
    'horizon.app.core.receivers.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service',
    'horizon.cluster.receivers.actions.workflow'
  ];

  function createService(
    $location, policy, senlin, basePath, resourceType, actionResult, gettext,
    modal, toast, workflow
  ) {

    var message = {
      success: gettext('Receiver %s was successfully created.')
    };

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function perform() {
      // modal title, buttons
      var title, submitText, submitIcon, helpUrl;
      title = gettext('Create Receiver');
      submitText = gettext('Create');
      submitIcon = 'fa fa-check';
      helpUrl = basePath + 'actions/receiver.help.html';

      var config = workflow.init('create', title, submitText, submitIcon, helpUrl);
      return modal.open(config).then(submit);
    }

    function allowed() {
      return policy.ifAllowed({ rules: [['cluster', 'receivers:create']] });
    }

    function submit(context) {
      delete context.model.id;
      return senlin.createReceiver(context.model, false).then(success, true);
    }

    function success(response) {
      toast.add('success', interpolate(message.success, [response.data.name]));
      var result = actionResult.getActionResult()
                   .created(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.created.length > 0) {
        $location.path("/cluster/receivers");
      } else {
        return result.result;
      }
    }
  }
})();

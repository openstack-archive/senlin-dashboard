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
   * @name horizon.cluster.clusters.actions.create.service
   * @description
   * Service for the cluster cluster create modal
   */
  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.update.service', updateService);

  updateService.$inject = [
    '$location',
    'horizon.app.core.clusters.basePath',
    'horizon.app.core.clusters.resourceType',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service',
    'horizon.cluster.clusters.actions.workflow'
  ];

  function updateService(
    $location, basePath, resourceType, policy, senlin, actionResult, gettext,
    modal, toast, workflow
  ) {

    var message = {
      success: gettext('Cluster %s was successfully updated.')
    };

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function perform(selected) {
      // modal title, buttons
      var title, submitText, helpUrl;
      title = gettext('Update Cluster');
      submitText = gettext('Update');
      helpUrl = basePath + 'actions/update/cluster.help.html';

      var config = workflow.init('update', title, submitText, helpUrl);

      // load current data
      senlin.getCluster(selected.id).then(onLoad);
      function onLoad(response) {
        config.model.id = response.data.id;
        config.model.name = response.data.name;
        config.model.profile_id = response.data.profile_id;
        config.model.min_size = response.data.min_size;
        config.model.max_size = response.data.max_size;
        config.model.desired_capacity = response.data.desired_capacity;
        config.model.timeout = response.data.timeout;
        config.model.metadata = response.data.metadata;
      }

      return modal.open(config).then(submit);
    }

    function allowed() {
      return policy.ifAllowed({ rules: [['cluster', 'clusters:update']] });
    }

    function submit(context) {
      var id = context.model.id;
      delete context.model.id;
      delete context.model.min_size;
      delete context.model.max_size;
      delete context.model.desired_capacity;
      return senlin.updateCluster(id, context.model, false).then(success, true);
    }

    function success(response) {
      toast.add('success', interpolate(message.success, [response.data.name]));
      var result = actionResult.getActionResult()
                   .updated(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.updated.length > 0) {
        $location.path("/cluster");
      } else {
        return result.result;
      }
    }
  }
})();

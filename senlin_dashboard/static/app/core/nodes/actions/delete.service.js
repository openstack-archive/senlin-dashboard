/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
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
    .module('horizon.cluster.nodes')
    .factory('horizon.cluster.nodes.actions.delete.service', deleteService);

  deleteService.$inject = [
    '$q',
    '$location',
    '$rootScope',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.modal.deleteModalService',
    'horizon.framework.widgets.table.events',
    'horizon.framework.widgets.toast.service',
    'horizon.app.core.nodes.resourceType'
  ];

  /*
   * @ngdoc factory
   * @name horizon.app.core.nodes.actions.delete.service
   *
   * @Description
   * Brings up the delete nodes confirmation modal dialog.

   * On submit, delete given nodes.
   * On cancel, do nothing.
   */
  function deleteService(
    $q,
    $location,
    $rootScope,
    policyService,
    senlin,
    actionResultService,
    gettext,
    $qExtensions,
    deleteModal,
    tableEvents,
    toast,
    nodesResourceType
  ) {
    var scope, context;
    var notAllowedMessage = gettext("You are not allowed to delete nodes: %s");

    var service = {
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function perform(items, newScope) {
      scope = newScope;
      var nodes = angular.isArray(items) ? items : [items];
      context = { };
      context.labels = labelize(nodes.length);
      context.deleteEntity = deleteNode;
      return $qExtensions.allSettled(nodes.map(checkPermission)).then(afterCheck);
    }

    function allowed() {
      return policyService.ifAllowed({ rules: [['cluster', 'nodes:delete']] });
    }

    function checkPermission(node) {
      return {promise: allowed(), context: node};
    }

    function afterCheck(result) {
      var outcome = $q.reject();  // Reject the promise by default
      if (result.fail.length > 0) {
        toast.add('error', getMessage(notAllowedMessage, result.fail));
        outcome = $q.reject(result.fail);
      }
      if (result.pass.length > 0) {
        outcome = deleteModal.open(scope, result.pass.map(getEntity), context).then(createResult);
      }
      return outcome;
    }

    function createResult(deleteModalResult) {
      var result = actionResultService.getActionResult();
      deleteModalResult.pass.forEach(function markDeleted(item) {
        result.deleted(nodesResourceType, getEntity(item).id);
      });
      deleteModalResult.fail.forEach(function markFailed(item) {
        result.failed(nodesResourceType, getEntity(item).id);
      });
      var indexPath = '/cluster/nodes';
      var currentPath = $location.path();
      if (result.result.failed.length === 0 && result.result.deleted.length > 0 &&
          currentPath !== indexPath) {
        $location.path(indexPath);
      } else {
        $rootScope.$broadcast(tableEvents.CLEAR_SELECTIONS);
        return result.result;
      }
    }

    function labelize(count) {
      return {

        title: ngettext(
          'Confirm Delete Node',
          'Confirm Delete Nodes', count),

        message: ngettext(
          'You have selected "%s". Deleted Node is not recoverable.',
          'You have selected "%s". Deleted Nodes are not recoverable.', count),

        submit: ngettext(
          'Delete Node',
          'Delete Nodes', count),

        success: ngettext(
          'Deleted Node: %s.',
          'Deleted Nodes: %s.', count),

        error: ngettext(
          'Unable to delete Node: %s.',
          'Unable to delete Nodes: %s.', count)
      };
    }

    function deleteNode(node) {
      return senlin.deleteNode(node, true);
    }

    function getMessage(message, entities) {
      return interpolate(message, [entities.map(getName).join(", ")]);
    }

    function getName(result) {
      return getEntity(result).name;
    }

    function getEntity(result) {
      return result.context;
    }
  }
})();

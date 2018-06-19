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
    .module('horizon.cluster.clusters')
    .factory('horizon.cluster.clusters.actions.delete.service', deleteClusterService);

  deleteClusterService.$inject = [
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
    'horizon.app.core.clusters.resourceType'
  ];

  /*
   * @ngdoc factory
   * @name horizon.app.core.clusters.actions.delete.service
   *
   * @Description
   * Brings up the delete clusters confirmation modal dialog.

   * On submit, delete given clusters.
   * On cancel, do nothing.
   */
  function deleteClusterService(
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
    clustersResourceType
  ) {
    var scope, context;
    var notAllowedMessage = gettext("You are not allowed to delete clusters: %s");

    var service = {
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function perform(items, newScope) {
      scope = newScope;
      var clusters = angular.isArray(items) ? items : [items];
      context = { };
      context.labels = labelize(clusters.length);
      context.deleteEntity = deleteCluster;
      return $qExtensions.allSettled(clusters.map(checkPermission)).then(afterCheck);
    }

    function allowed() {
      return policyService.ifAllowed({ rules: [['cluster', 'clusters:delete']] });
    }

    function checkPermission(cluster) {
      return {promise: allowed(), context: cluster};
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
      // To make the result of this action generically useful, reformat the return
      // from the deleteModal into a standard form
      var actionResult = actionResultService.getActionResult();
      deleteModalResult.pass.forEach(function markDeleted(item) {
        actionResult.deleted(clustersResourceType, getEntity(item).id);
      });
      deleteModalResult.fail.forEach(function markFailed(item) {
        actionResult.failed(clustersResourceType, getEntity(item).id);
      });
      var indexPath = '/cluster';
      var currentPath = $location.path();
      if (actionResult.result.failed.length === 0 && actionResult.result.deleted.length > 0 &&
          currentPath !== indexPath) {
        $location.path(indexPath);
      } else {
        $rootScope.$broadcast(tableEvents.CLEAR_SELECTIONS);
        return actionResult.result;
      }
    }

    function labelize(count) {
      return {

        title: ngettext(
          'Confirm Delete Cluster',
          'Confirm Delete Clusters', count),

        message: ngettext(
          'You have selected "%s". Deleted Cluster is not recoverable.',
          'You have selected "%s". Deleted Clusters are not recoverable.', count),

        submit: ngettext(
          'Delete Cluster',
          'Delete Clusters', count),

        success: ngettext(
          'Deleted Cluster: %s.',
          'Deleted Clusters: %s.', count),

        error: ngettext(
          'Unable to delete Cluster: %s.',
          'Unable to delete Clusters: %s.', count)
      };
    }

    function deleteCluster(cluster) {
      return senlin.deleteCluster(cluster, true);
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

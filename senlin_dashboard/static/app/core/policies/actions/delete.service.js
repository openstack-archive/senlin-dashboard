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
    .module('horizon.cluster.policies')
    .factory('horizon.cluster.policies.actions.delete.service', deletePolicyService);

  deletePolicyService.$inject = [
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
    'horizon.app.core.policies.resourceType'
  ];

  /*
   * @ngdoc factory
   * @name horizon.app.core.policies.actions.delete.service
   *
   * @Description
   * Brings up the delete policies confirmation modal dialog.

   * On submit, delete given policies.
   * On cancel, do nothing.
   */
  function deletePolicyService(
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
    policiesResourceType
  ) {
    var scope, context;
    var notAllowedMessage = gettext("You are not allowed to delete policies: %s");

    var service = {
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function perform(items, newScope) {
      scope = newScope;
      var policies = angular.isArray(items) ? items : [items];
      context = { };
      context.labels = labelize(policies.length);
      context.deleteEntity = deletePolicy;
      return $qExtensions.allSettled(policies.map(checkPermission)).then(afterCheck);
    }

    function allowed() {
      return policyService.ifAllowed({ rules: [['cluster', 'policies:delete']] });
    }

    function checkPermission(policy) {
      return {promise: allowed(), context: policy};
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
        actionResult.deleted(policiesResourceType, getEntity(item).id);
      });
      deleteModalResult.fail.forEach(function markFailed(item) {
        actionResult.failed(policiesResourceType, getEntity(item).id);
      });
      var indexPath = '/cluster/policies';
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
          'Confirm Delete Policy',
          'Confirm Delete Policies', count),

        message: ngettext(
          'You have selected "%s". Deleted Policy is not recoverable.',
          'You have selected "%s". Deleted Policies are not recoverable.', count),

        submit: ngettext(
          'Delete Policy',
          'Delete Policies', count),

        success: ngettext(
          'Deleted Policy: %s.',
          'Deleted Policies: %s.', count),

        error: ngettext(
          'Unable to delete Policy: %s.',
          'Unable to delete Policies: %s.', count)
      };
    }

    function deletePolicy(policy) {
      return senlin.deletePolicy(policy, true);
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

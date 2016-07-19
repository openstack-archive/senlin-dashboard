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
    .module('horizon.cluster.receivers')
    .factory('horizon.app.core.receivers.actions.delete.service', deleteReceiverService);

  deleteReceiverService.$inject = [
    '$q',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.modal.deleteModalService',
    'horizon.framework.widgets.toast.service',
    'horizon.app.core.receivers.resourceType'
  ];

  /*
   * @ngdoc factory
   * @name horizon.app.core.receivers.actions.delete.service
   *
   * @Description
   * Brings up the delete receivers confirmation modal dialog.

   * On submit, delete given receivers.
   * On cancel, do nothing.
   */
  function deleteReceiverService(
    $q,
    senlin,
    actionResultService,
    gettext,
    $qExtensions,
    deleteModal,
    toast,
    receiversResourceType
  ) {
    var scope, context;
    var notAllowedMessage = gettext("You are not allowed to delete receivers: %s");

    var service = {
      initScope: initScope,
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function initScope(newScope) {
      scope = newScope;
      context = { };
    }

    function perform(items) {
      var receivers = angular.isArray(items) ? items : [items];
      context.labels = labelize(receivers.length);
      context.deleteEntity = deleteReceiver;
      return $qExtensions.allSettled(receivers.map(checkPermission)).then(afterCheck);
    }

    function allowed() {
      return $q.all([
        $qExtensions.booleanAsPromise(true)
      ]);
    }

    function checkPermission(receiver) {
      return {promise: allowed(receiver), context: receiver};
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
        actionResult.deleted(receiversResourceType, getEntity(item).id);
      });
      deleteModalResult.fail.forEach(function markFailed(item) {
        actionResult.failed(receiversResourceType, getEntity(item).id);
      });
      return actionResult.result;
    }

    function labelize(count) {
      return {

        title: ngettext(
          'Confirm Delete Receiver',
          'Confirm Delete Receivers', count),

        message: ngettext(
          'You have selected "%s". Deleted Receiver is not recoverable.',
          'You have selected "%s". Deleted Receivers are not recoverable.', count),

        submit: ngettext(
          'Delete Receiver',
          'Delete Receivers', count),

        success: ngettext(
          'Deleted Receiver: %s.',
          'Deleted Receivers: %s.', count),

        error: ngettext(
          'Unable to delete Receiver: %s.',
          'Unable to delete Receivers: %s.', count)
      };
    }

    function deleteReceiver(receiver) {
      return senlin.deleteReceiver(receiver, true);
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

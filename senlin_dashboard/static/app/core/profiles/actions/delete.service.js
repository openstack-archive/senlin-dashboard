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
    .module('horizon.cluster.profiles')
    .factory('horizon.cluster.profiles.actions.delete.service', deleteService);

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
    'horizon.app.core.profiles.resourceType'
  ];

  /*
   * @ngdoc factory
   * @name horizon.app.core.profiles.actions.delete.service
   *
   * @Description
   * Brings up the delete profiles confirmation modal dialog.

   * On submit, delete given profiles.
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
    profilesResourceType
  ) {
    var scope, context;
    var notAllowedMessage = gettext("You are not allowed to delete profiles: %s");

    var service = {
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function perform(items, newScope) {
      scope = newScope;
      var profiles = angular.isArray(items) ? items : [items];
      context = { };
      context.labels = labelize(profiles.length);
      context.deleteEntity = deleteProfile;
      return $qExtensions.allSettled(profiles.map(checkPermission)).then(afterCheck);
    }

    function allowed() {
      return policyService.ifAllowed({ rules: [['cluster', 'profiles:delete']] });
    }

    function checkPermission(profile) {
      return {promise: allowed(), context: profile};
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
        result.deleted(profilesResourceType, getEntity(item).id);
      });
      deleteModalResult.fail.forEach(function markFailed(item) {
        result.failed(profilesResourceType, getEntity(item).id);
      });
      var indexPath = '/cluster/profiles';
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
          'Confirm Delete Profile',
          'Confirm Delete Profiles', count),

        message: ngettext(
          'You have selected "%s". Deleted Profile is not recoverable.',
          'You have selected "%s". Deleted Profiles are not recoverable.', count),

        submit: ngettext(
          'Delete Profile',
          'Delete Profiles', count),

        success: ngettext(
          'Deleted Profile: %s.',
          'Deleted Profiles: %s.', count),

        error: ngettext(
          'Unable to delete Profile: %s.',
          'Unable to delete Profiles: %s.', count)
      };
    }

    function deleteProfile(profile) {
      return senlin.deleteProfile(profile, true);
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

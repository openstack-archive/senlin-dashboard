/*
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
   * @ngdoc overview
   * @ngname horizon.cluster.profiles.actions
   *
   * @description
   * Provides all of the actions for profiles.
   */
  angular.module('horizon.cluster.profiles.actions', [
    'horizon.framework.conf',
    'horizon.cluster.profiles'
  ])
    .run(registerProfileActions);

  registerProfileActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.profiles.actions.create.service',
    'horizon.cluster.profiles.actions.update.service',
    'horizon.cluster.profiles.actions.delete.service',
    'horizon.app.core.profiles.resourceType'
  ];

  function registerProfileActions(
    registry,
    createProfileService,
    updateProfileService,
    deleteProfileService,
    profileResourceType
  ) {
    var resourceType = registry.getResourceType(profileResourceType);

    resourceType.globalActions
      .append({
        id: 'createProfileAction',
        service: createProfileService,
        template: {
          text: gettext('Create Profile'),
          type: 'create'
        }
      });

    resourceType.itemActions
      .append({
        id: 'updateProfileAction',
        service: updateProfileService,
        template: {
          text: gettext('Update Profile'),
          type: 'row'
        }
      })
      .append({
        id: 'deleteProfileAction',
        service: deleteProfileService,
        template: {
          text: gettext('Delete Profile'),
          type: 'delete'
        }
      });

    resourceType.batchActions
      .append({
        id: 'batchDeleteProfileAction',
        service: deleteProfileService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Profiles')
        }
      });
  }

})();

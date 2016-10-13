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
   * @ngname horizon.cluster.profiles.details
   *
   * @description
   * Provides details features for senlin profile.
   */
  angular.module('horizon.cluster.profiles.details', [
    'horizon.framework.conf',
    'horizon.app.core'
  ])
   .run(registerProfileDetails);

  registerProfileDetails.$inject = [
    'horizon.app.core.profiles.basePath',
    'horizon.app.core.profiles.resourceType',
    'horizon.cluster.profiles.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function registerProfileDetails(
    basePath,
    profileResourceType,
    profileService,
    registry
  ) {
    registry.getResourceType(profileResourceType)
      .setLoadFunction(profileService.getProfilePromise)
      .detailsViews.append({
        id: 'profileDetailsOverview',
        name: gettext('Overview'),
        template: basePath + 'details/overview.html'
      });
  }

})();

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
   * @ngname horizon.cluster.clusters.details
   *
   * @description
   * Provides details features for senlin cluster.
   */
  angular.module('horizon.cluster.clusters.details', [
    'horizon.framework.conf',
    'horizon.app.core'
  ])
   .run(registerClusterDetails);

  registerClusterDetails.$inject = [
    'horizon.app.core.clusters.basePath',
    'horizon.app.core.clusters.resourceType',
    'horizon.cluster.clusters.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function registerClusterDetails(
    basePath,
    clusterResourceType,
    clusterService,
    registry
  ) {
    registry.getResourceType(clusterResourceType)
      .setLoadFunction(clusterService.getClusterPromise)
      .detailsViews.append({
        id: 'clusterDetailsOverview',
        name: gettext('Overview'),
        template: basePath + 'details/overview.html'
      });
  }

})();

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
   * @ngname horizon.cluster.clusters
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display clusters related content.
   */
  angular
    .module('horizon.cluster.clusters', [
      'ngRoute',
      'horizon.cluster.clusters.actions',
      'horizon.cluster.clusters.details'
    ])
    .constant('horizon.app.core.clusters.resourceType', 'OS::Senlin::Cluster')
    .constant('horizon.app.core.clusters.statuses', {
      INIT: gettext('INIT'),
      ACTIVE: gettext('ACTIVE'),
      ERROR: gettext('ERROR'),
      CRITICAL: gettext('CRITICAL'),
      WARNING: gettext('WARNING'),
      CREATING: gettext('CREATING'),
      UPDATING: gettext('UPDATING'),
      DELETING: gettext('DELETING'),
      RESIZING: gettext('RESIZING'),
      CHECKING: gettext('CHECKING'),
      RECOVERING: gettext('RECOVERING')
    })
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.clusters.service',
    'horizon.app.core.clusters.basePath',
    'horizon.app.core.clusters.resourceType',
    'horizon.app.core.clusters.statuses'
  ];

  function run(registry, clusterService, basePath, clusterResourceType, statuses) {
    registry.getResourceType(clusterResourceType)
      .setNames(gettext('Cluster'), gettext('Clusters'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setDefaultIndexUrl('/cluster/')
      .setProperties(clusterProperties(statuses))
      .setListFunction(clusterService.getClustersPromise)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: clusterService.getDetailsClusterPath
      })
      .append({
        id: 'status',
        priority: 1
      })
      .append({
        id: 'status_reason',
        priority: 2
      })
      .append({
        id: 'profile_name',
        priority: 2,
        urlFunction: clusterService.getDetailsProfilePath
      })
      .append({
        id: 'created_at',
        priority: 2
      })
      .append({
        id: 'updated_at',
        priority: 1
      });
  }

  function clusterProperties(statuses) {
    return {
      id: { label: gettext('ID'), filters: ['noValue']},
      name: { label: gettext('Name'), filters: ['noName']},
      status: { label: gettext('Status'), values: statuses, filters: ['noValue']},
      status_reason: { label: gettext('Status Reason')},
      profile_name: { label: gettext('Profile Name')},
      created_at: { label: gettext('Created'), filters: ['simpleDate']},
      updated_at: { label: gettext('Updated'), filters: ['simpleDate']}
    };
  }

  config.$inject = [
    '$provide',
    '$windowProvider',
    '$routeProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @param {Object} $routeProvider
   * @description Routes used by this module.
   * @returns {undefined} Returns nothing
   */
  function config($provide, $windowProvider, $routeProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'app/core/clusters/';
    $provide.constant('horizon.app.core.clusters.basePath', path);

    $routeProvider.when('/cluster', {
      templateUrl: path + 'panel.html'
    });
  }
})();

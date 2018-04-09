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
   * @ngname horizon.cluster.nodes
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display nodes related content.
   */
  angular
    .module('horizon.cluster.nodes', [
      'ngRoute',
      'horizon.cluster.nodes.details',
      'horizon.cluster.nodes.actions'
    ])
    .constant('horizon.app.core.nodes.resourceType', 'OS::Senlin::Node')
    .constant('horizon.app.core.nodes.statuses', {
      INIT: gettext('INIT'),
      ACTIVE: gettext('ACTIVE'),
      ERROR: gettext('ERROR'),
      WARNING: gettext('WARNING'),
      CREATING: gettext('CREATING'),
      UPDATING: gettext('UPDATING'),
      DELETING: gettext('DELETING'),
      RECOVERING: gettext('RECOVERING')
    })
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.nodes.basePath',
    'horizon.app.core.nodes.resourceType',
    'horizon.app.core.nodes.statuses',
    'horizon.cluster.nodes.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function run(senlin, basePath, nodeResourceType, statuses, nodeService, registry) {
    registry.getResourceType(nodeResourceType)
      .setNames(gettext('Node'), gettext('Nodes'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setDefaultIndexUrl('/cluster/nodes/')
      .setProperties(nodeProperties(statuses))
      .setListFunction(nodeService.getNodesPromise)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: nodeService.getDetailsPath
      })
      .append({
        id: 'profile_name',
        priority: 1
      })
      .append({
        id: 'physical_id',
        priority: 2
      })
      .append({
        id: 'role',
        priority: 2
      })
      .append({
        id: 'cluster_id',
        priority: 2
      })
      .append({
        id: 'status',
        priority: 1
      })
      .append({
        id: 'created_at',
        priority: 2
      })
      .append({
        id: 'updated_at',
        priority: 2
      });
    // for magic-search
    registry.getResourceType(nodeResourceType).filterFacets
      .append({
        label: gettext('Name'),
        name: 'name',
        singleton: true
      })
      .append({
        label: gettext('Profile Name'),
        name: 'profile_name',
        singleton: true
      })
      .append({
        label: gettext('Physical ID'),
        name: 'physical_id',
        singleton: true
      })
      .append({
        label: gettext('Role'),
        name: 'role',
        singleton: true
      })
      .append({
        label: gettext('Cluster ID'),
        name: 'cluster_id',
        singleton: true
      })
      .append({
        label: gettext('Status'),
        name: 'status',
        singleton: true
      });
  }

  function nodeProperties(statuses) {
    return {
      id: { label: gettext('ID'), filters: ['noValue'] },
      name: { label: gettext('Name'), filters: ['noName'] },
      profile_name: { label: gettext('Profile Name'), filters: ['noName'] },
      physical_id: { label: gettext('Physical ID'), filters: ['noValue'] },
      role: { label: gettext('Role'), filters: ['noValue'] },
      cluster_id: { label: gettext('Cluster ID'), filters: ['noValue'] },
      status: { label: gettext('Status'), values: statuses, filters: ['noValue'] },
      status_reason: { label: gettext('Status Reason'), filters: ['noValue'] },
      metadata: { label: gettext('Metadata'), filters: [] },
      created_at: { label: gettext('Created'), filters: ['simpleDate'] },
      updated_at: { label: gettext('Updated'), filters: ['simpleDate'] }
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
    var path = $windowProvider.$get().STATIC_URL + 'app/core/nodes/';
    $provide.constant('horizon.app.core.nodes.basePath', path);

    $routeProvider.when('/cluster/nodes', {
      templateUrl: path + 'panel.html'
    });
  }
})();

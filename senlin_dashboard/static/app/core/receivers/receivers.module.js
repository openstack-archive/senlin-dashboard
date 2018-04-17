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
   * @ngname horizon.cluster.receivers
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display receivers related content.
   */
  angular
    .module('horizon.cluster.receivers', [
      'ngRoute',
      'horizon.cluster.receivers.details',
      'horizon.cluster.receivers.actions'
    ])
    .constant('horizon.app.core.receivers.resourceType', 'OS::Senlin::Receiver')
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.app.core.receivers.basePath',
    'horizon.app.core.receivers.resourceType',
    'horizon.cluster.receivers.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function run(basePath, receiverResourceType, receiverService, registry) {
    registry.getResourceType(receiverResourceType)
      .setNames(gettext('Receiver'), gettext('Receivers'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setDefaultIndexUrl('/cluster/receivers/')
      .setProperties(receiverProperties())
      .setListFunction(receiverService.getReceiversPromise)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: receiverService.getDetailsPath
      })
      .append({
        id: 'type',
        priority: 1
      })
      .append({
        id: 'cluster_id',
        priority: 1
      })
      .append({
        id: 'action',
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
    registry.getResourceType(receiverResourceType).filterFacets
      .append({
        label: gettext('Name'),
        name: 'name',
        singleton: true
      })
      .append({
        label: gettext('Type'),
        name: 'type',
        singleton: true
      })
      .append({
        label: gettext('Cluster ID'),
        name: 'cluster_id',
        singleton: true
      })
      .append({
        label: gettext('Action'),
        name: 'action',
        singleton: true
      })
      .append({
        label: gettext('Channel'),
        name: 'channel',
        singleton: true
      });
  }

  function receiverProperties() {
    return {
      id: { label: gettext('ID'), filters: ['noValue'] },
      name: { label: gettext('Name'), filters: ['noName'] },
      type: { label: gettext('Type'), filters: ['noValue'] },
      cluster_id: { label: gettext('Cluster ID'), filters: ['noValue'] },
      action: { label: gettext('Action'), filters: ['noValue'] },
      params: { label: gettext('Parameters'), filters: ['noValue'] },
      channel: { label: gettext('Channel'), filters: ['noValue'] },
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
    var path = $windowProvider.$get().STATIC_URL + 'app/core/receivers/';
    $provide.constant('horizon.app.core.receivers.basePath', path);

    $routeProvider.when('/cluster/receivers', {
      templateUrl: path + 'panel.html'
    });
  }
})();

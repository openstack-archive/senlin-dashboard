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
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.receivers.basePath',
    'horizon.app.core.receivers.resourceType'
  ];

  function run(registry, senlin, basePath, receiverResourceType) {
    registry.getResourceType(receiverResourceType)
      .setNames(gettext('Receiver'), gettext('Receivers'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setProperty('name', {
        label: gettext('Name')
      })
      .setProperty('id', {
        label: gettext('ID')
      })
      .setProperty('type', {
        label: gettext('Type')
      })
      .setProperty('cluster_id', {
        label: gettext('Cluster ID')
      })
      .setProperty('action', {
        label: gettext('Action')
      })
      .setProperty('created_at', {
        label: gettext('Created')
      })
      .setProperty('updated_at', {
        label: gettext('Updated')
      })
      .setProperty('channel', {
        label: gettext('Channel')
      })
      .setListFunction(listFunction)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: urlFunction
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
      });

    function listFunction() {
      return senlin.getReceivers();
    }

    function urlFunction(item) {
      return 'project/ngdetails/OS::Senlin::Receiver/' + item.id;
    }
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

    $routeProvider.when('/cluster/ngreceivers/', {
      templateUrl: path + 'panel.html'
    });
  }
})();

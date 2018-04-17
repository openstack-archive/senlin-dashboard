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
   * @ngname horizon.cluster.policies
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display policies related content.
   */
  angular
    .module('horizon.cluster.policies', [
      'ngRoute',
      'horizon.cluster.policies.details',
      'horizon.cluster.policies.actions'
    ])
    .constant('horizon.app.core.policies.resourceType', 'OS::Senlin::Policy')
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.app.core.policies.basePath',
    'horizon.app.core.policies.resourceType',
    'horizon.cluster.policies.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function run(basePath, policyResourceType, policyService, registry) {
    registry.getResourceType(policyResourceType)
      .setNames(gettext('Policy'), gettext('Policies'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setDefaultIndexUrl('/cluster/policies/')
      .setProperties(policyProperties())
      .setListFunction(policyService.getPoliciesPromise)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: policyService.getDetailsPath
      })
      .append({
        id: 'type',
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
    registry.getResourceType(policyResourceType).filterFacets
      .append({
        label: gettext('Name'),
        name: 'name',
        singleton: true
      })
      .append({
        label: gettext('Type'),
        name: 'type',
        singleton: true
      });
  }

  function policyProperties() {
    return {
      id: { label: gettext('ID'), filters: ['noValue'] },
      name: { label: gettext('Name'), filters: ['noName'] },
      type: { label: gettext('Type'), filters: ['noValue'] },
      spec: { label: gettext('Spec') },
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
    var path = $windowProvider.$get().STATIC_URL + 'app/core/policies/';
    $provide.constant('horizon.app.core.policies.basePath', path);

    $routeProvider.when('/cluster/policies', {
      templateUrl: path + 'panel.html'
    });
  }
})();

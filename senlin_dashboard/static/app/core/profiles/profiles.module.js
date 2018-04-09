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
   * @ngname horizon.cluster.profiles
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display profiles related content.
   */
  angular
    .module('horizon.cluster.profiles', [
      'ngRoute',
      'horizon.cluster.profiles.details',
      'horizon.cluster.profiles.actions'
    ])
    .constant('horizon.app.core.profiles.resourceType', 'OS::Senlin::Profile')
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.profiles.service',
    'horizon.app.core.profiles.basePath',
    'horizon.app.core.profiles.resourceType'

  ];

  function run(registry, profileService, basePath, profileResourceType) {
    registry.getResourceType(profileResourceType)
      .setNames(gettext('Profile'), gettext('Profiles'))
      .setSummaryTemplateUrl(basePath + 'details/drawer.html')
      .setDefaultIndexUrl('/cluster/profiles/')
      .setProperties(profileProperties())
      .setListFunction(profileService.getProfilesPromise)
      .tableColumns
      .append({
        id: 'name',
        priority: 1,
        sortDefault: true,
        urlFunction: profileService.getDetailsPath
      })
      .append({
        id: 'type',
        priority: 1
      })
      .append({
        id: 'created_at',
        priority: 1
      })
      .append({
        id: 'updated_at',
        priority: 1
      });

    // for magic-search
    registry.getResourceType(profileResourceType).filterFacets
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

  function profileProperties() {
    return {
      id: { label: gettext('ID'), filters: ['noValue'] },
      name: { label: gettext('Name'), filters: ['noName'] },
      type: { label: gettext('Type'), filters: ['noValue'] },
      spec: { label: gettext('Spec')},
      metadata: { label: gettext('Metadata')},
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
    var path = $windowProvider.$get().STATIC_URL + 'app/core/profiles/';
    $provide.constant('horizon.app.core.profiles.basePath', path);

    $routeProvider.when('/cluster/profiles', {
      templateUrl: path + 'panel.html'
    });
  }
})();

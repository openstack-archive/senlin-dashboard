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
   * @ngname horizon.cluster.events
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display events related content.
   */
  angular
    .module('horizon.cluster.events', [])
    .constant('horizon.app.core.events.resourceType', 'OS::Senlin::Event')
    .run(run)
    .config(config);

  run.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.events.basePath',
    'horizon.app.core.events.resourceType',
    'horizon.cluster.events.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function run(senlin, basePath, eventResourceType, eventService, registry) {
    registry.getResourceType(eventResourceType)
      .setNames(gettext('Event'), gettext('Events'))
      .setSummaryTemplateUrl(basePath + 'events_drawer.html')
      .setProperties(eventProperties())
      .setListFunction(eventService.getEventsPromise)
      .tableColumns
      .append({
        id: 'generated_at',
        priority: 1,
        sortDefault: true
      })
      .append({
        id: 'obj_id',
        priority: 2
      })
      .append({
        id: 'obj_name',
        priority: 1
      })
      .append({
        id: 'action',
        priority: 1
      })
      .append({
        id: 'status',
        priority: 1
      });
    // for magic-search
    registry.getResourceType(eventResourceType).filterFacets
      .append({
        label: gettext('Object Name'),
        name: 'obj_name',
        singleton: true
      })
      .append({
        label: gettext('Object ID'),
        name: 'obj_id',
        singleton: true
      })
      .append({
        label: gettext('Action'),
        name: 'action',
        singleton: true
      })
      .append({
        label: gettext('Status'),
        name: 'status',
        singleton: true
      });
  }

  function eventProperties() {
    return {
      id: { label: gettext('ID'), filters: ['noValue'] },
      generated_at: { label: gettext('Generated'), filters: ['simpleDate'] },
      obj_id: { label: gettext('Object ID'), filters: ['noValue'] },
      obj_name: { label: gettext('Object Name'), filters: ['noName'] },
      action: { label: gettext('Action'), filters: ['noValue'] },
      status: { label: gettext('Status'), filters: ['noValue'] },
      status_reason: { label: gettext('Status Reason'), filters: ['noValue'] }
    };
  }

  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Basepath used by this module.
   * @returns {undefined} Returns nothing
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'app/core/events/';
    $provide.constant('horizon.app.core.events.basePath', path);
  }
})();

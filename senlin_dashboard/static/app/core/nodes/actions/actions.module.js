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
   * @ngname horizon.cluster.nodes.actions
   *
   * @description
   * Provides all of the actions for nodes.
   */
  angular.module('horizon.cluster.nodes.actions', [
    'horizon.framework.conf',
    'horizon.cluster.nodes'
  ])
    .run(registerNodeActions);

  registerNodeActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.nodes.actions.delete.service',
    'horizon.app.core.nodes.resourceType'
  ];

  function registerNodeActions(
    registry,
    deleteNodeService,
    nodeResourceType
  ) {
    var resourceType = registry.getResourceType(nodeResourceType);

    resourceType.itemActions
      .append({
        id: 'deleteNodeAction',
        service: deleteNodeService,
        template: {
          text: gettext('Delete Node'),
          type: 'delete'
        }
      });

    resourceType.batchActions
      .append({
        id: 'batchDeleteNodeAction',
        service: deleteNodeService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Nodes')
        }
      });
  }

})();

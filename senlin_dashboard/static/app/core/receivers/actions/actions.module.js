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
   * @ngname horizon.cluster.receivers.actions
   *
   * @description
   * Provides all of the actions for receivers.
   */
  angular.module('horizon.cluster.receivers.actions', [
    'horizon.framework.conf',
    'horizon.cluster.receivers'
  ])
    .run(registerReceiverActions);

  registerReceiverActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.app.core.receivers.actions.delete.service',
    'horizon.app.core.receivers.resourceType'
  ];

  function registerReceiverActions(
    registry,
    deleteReceiverService,
    receiverResourceType
  ) {
    var receiverResourceType = registry.getResourceType(receiverResourceType);
    receiverResourceType.itemActions
      .append({
        id: 'deleteReceiverAction',
        service: deleteReceiverService,
        template: {
          text: gettext('Delete Receiver'),
          type: 'delete'
        }
      });

    receiverResourceType.batchActions
      .append({
        id: 'batchDeleteReceiverAction',
        service: deleteReceiverService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Receivers')
        }
      });
  }

})();

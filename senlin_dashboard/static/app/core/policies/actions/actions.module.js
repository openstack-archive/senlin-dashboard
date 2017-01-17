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
   * @ngname horizon.cluster.policies.actions
   *
   * @description
   * Provides all of the actions for policies.
   */
  angular.module('horizon.cluster.policies.actions', [
    'horizon.framework.conf',
    'horizon.cluster.policies'
  ])
    .run(registerPolicyActions);

  registerPolicyActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.policies.actions.create.service',
    'horizon.cluster.policies.actions.delete.service',
    'horizon.cluster.policies.actions.update.service',
    'horizon.app.core.policies.resourceType'
  ];

  function registerPolicyActions(
    registry,
    createPolicyService,
    deletePolicyService,
    updatePolicyService,
    policyResourceType
  ) {
    var policyResource = registry.getResourceType(policyResourceType);

    policyResource.globalActions
      .append({
        id: 'createPolicyAction',
        service: createPolicyService,
        template: {
          text: gettext('Create Policy'),
          type: 'create'
        }
      });

    policyResource.batchActions
      .append({
        id: 'batchDeletePolicyAction',
        service: deletePolicyService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Policies')
        }
      });

    policyResource.itemActions
      .append({
        id: 'updatePolicyAction',
        service: updatePolicyService,
        template: {
          text: gettext('Update Policy'),
          type: 'row'
        }
      })
      .append({
        id: 'deletePolicyAction',
        service: deletePolicyService,
        template: {
          text: gettext('Delete Policy'),
          type: 'delete'
        }
      });
  }
})();

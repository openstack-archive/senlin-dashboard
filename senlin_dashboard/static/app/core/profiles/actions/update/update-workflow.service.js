/**
 * Copyright 2016 NEC Corporation
 *
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
   * @ngdoc factory
   * @name horizon.cluster.profiles.actions.update.service.workflow
   * @ngController
   *
   * @description
   * Workflow for updating a cluster profile
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .factory('horizon.cluster.profiles.actions.update.service.workflow', ProfileWorkflow);

  ProfileWorkflow.$inject = [
    'horizon.app.core.profiles.basePath',
    'horizon.app.core.workflow.factory',
    'horizon.framework.util.i18n.gettext'
  ];

  function ProfileWorkflow(basePath, workflowService, gettext) {
    return workflowService({
      title: gettext('Update Profile'),
      steps: [
        {
          title: gettext('Info'),
          templateUrl: basePath + 'actions/create/profile.html',
          helpUrl: basePath + 'actions/update/profile.help.html',
          formName: 'profileForm'
        }
      ],
      btnText: {
        finish: gettext('Update')
      },
      btnIcon: {
        finish: 'fa fa-check'
      }
    });
  }
})();

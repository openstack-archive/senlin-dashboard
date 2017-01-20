/*
 * Copyright 2016 Symantec Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.cluster.clusters.actions')
    .controller('ManagePolicyController', ManagePolicyController);

  ManagePolicyController.$inject = [
    'horizon.cluster.clusters.actions.manage-policy.model',
    'horizon.app.core.clusters.basePath'
  ];

  /**
   * @ngdoc controller
   * @name ManagePolicyController
   * @param {Object} managePolicyModel
   * @param {string} basePath
   * @description
   * Allows selection of policies on selected cluster.
   * @returns {undefined} No return value
   */
  function ManagePolicyController(managePolicyModel, basePath) {
    var ctrl = this;

    ctrl.tableData = {
      available: managePolicyModel.policies,
      allocated: managePolicyModel.newSpec.policies,
      displayedAvailable: [],
      displayedAllocated: []
    };

    ctrl.tableDetails = basePath + 'actions/manage-policy/manage-policy-detail.html';

    ctrl.tableHelp = {
      /*eslint-disable max-len */
      noneAllocText: gettext('Select policies from the available policies below.'),
      /*eslint-enable max-len */
      availHelpText: gettext('')
    };

    ctrl.tableLimits = {
      maxAllocation: ctrl.tableData.available.length
    };

    ctrl.filterFacets = [
      {
        label: gettext('Name'),
        name: 'name',
        singleton: true
      }
    ];
  }
})();

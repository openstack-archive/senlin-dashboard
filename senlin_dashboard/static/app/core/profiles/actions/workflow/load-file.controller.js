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
   * @ngdoc controller
   * @name horizon.cluster.profiles.actions.workflow.loadFileController
   * @ngController
   *
   * @description
   * Controller for the loading file
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .controller('horizon.cluster.profiles.actions.workflow.loadFileController',
      loadFileController);

  loadFileController.$inject = [
    '$scope'
  ];

  function loadFileController($scope) {
    var ctrl = this;
    ctrl.filename = "";
    ctrl.changeFile = changeFile;

    ////

    function changeFile(files) {
      if (files.length) {
        var reader = new FileReader();
        reader.onload = function() {
          $scope.model.spec = reader.result;
          $scope.$emit('schemaFormRedraw');
        };
        reader.readAsText(files[0]);
      }
    }
  }
})();

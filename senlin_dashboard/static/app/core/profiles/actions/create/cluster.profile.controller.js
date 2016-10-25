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
   * @name horizon.cluster.profiles.actions.create.createProfileController
   * @ngController
   *
   * @description
   * Controller for the cluster profile step in create workflow
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .controller('horizon.cluster.profiles.actions.create.createProfileController',
      createProfileController);

  createProfileController.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.cluster.profiles.actions.create.model'
  ];

  function createProfileController(senlin, model) {
    var ctrl = this;
    ctrl.changeFile = changeFile;
    ctrl.changeSourceType = changeSourceType;
    ctrl.specfile = null;
    ctrl.source_type = null;

    ctrl.toggleOptions = [
      { label: gettext('File'), value: 'file' },
      { label: gettext('Direct'), value: 'direct' }
    ];

    init();

    ////

    function init() {
      ctrl.source_type = ctrl.toggleOptions[0].value;
    }

    function changeFile(files) {
      if (files.length) {
        var reader = new FileReader();
        reader.readAsText(files[0]);
        reader.onload = function() {
          model.newProfileSpec.spec = reader.result;
          //ctrl.specfile = files[0];
        };
      } else {
        model.newProfileSpec.spec = "";
        //ctrl.specfile = null;
      }
    }

    function changeSourceType() {
      model.newProfileSpec.spec = "";
    }
  }
})();

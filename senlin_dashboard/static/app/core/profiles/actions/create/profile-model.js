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

  angular
    .module('horizon.cluster.profiles.actions')
    .factory('horizon.cluster.profiles.actions.create.model', ProfileModel);

  ProfileModel.$inject = [
    'horizon.app.core.openstack-service-api.senlin'
  ];

  function ProfileModel(senlin) {
    var model = {
      newProfileSpec: {},
      init: init,
      createProfile: createProfile
    };

    function init() {
      initNewProfileSpec();
    }

    ////

    function initNewProfileSpec() {
      model.newProfileSpec = {
        name: null,
        metadata: null,
        spec: null
      };
    }

    function createProfile() {
      var finalSpec = angular.copy(model.newProfileSpec);

      cleanNullProperties(finalSpec);

      return senlin.createProfile(finalSpec, true);
    }

    function cleanNullProperties(finalSpec) {
      // Initially clean fields that don't have any value.
      for (var key in finalSpec) {
        if (finalSpec.hasOwnProperty(key) && finalSpec[key] === null) {
          delete finalSpec[key];
        }
      }
    }

    return model;
  }
})();

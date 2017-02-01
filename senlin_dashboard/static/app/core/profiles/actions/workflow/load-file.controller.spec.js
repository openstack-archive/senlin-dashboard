/**
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
  describe('horizon.cluster.profiles.actions.workflow.loadFileController', function() {
    var controller, $scope;

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core.openstack-service-api'));
    beforeEach(module('horizon.cluster.profiles.actions'));

    beforeEach(inject(function ($injector, _$rootScope_) {
      $scope = _$rootScope_.$new();
      $scope.model = {
        spec: ''
      };
      controller = $injector.get('$controller');
      controller(
        'horizon.cluster.profiles.actions.workflow.loadFileController',
        {
          $scope: $scope
        });
    }));

    it('should scope is changed by load spec yaml file', function() {
      $scope.$apply();
      expect($scope.model.spec).toBe('');
    });
  });
})();

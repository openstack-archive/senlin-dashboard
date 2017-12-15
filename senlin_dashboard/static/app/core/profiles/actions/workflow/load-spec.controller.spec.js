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
  describe('horizon.cluster.profiles.actions.workflow.loadSpecController', function() {
    var ctrl, $scope;

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core.openstack-service-api'));
    beforeEach(module('horizon.cluster.profiles.actions'));

    beforeEach(inject(function ($controller, _$rootScope_) {
      $scope = _$rootScope_.$new();
      $scope.schema = {
        properties: {
          spec: {
            title: "title"
          }
        }
      };
      $scope.model = {
        spec: ''
      };
      ctrl = $controller(
        'horizon.cluster.profiles.actions.workflow.loadSpecController',
        {
          $scope: $scope
        });
    }));

    it('should title is set', function() {
      $scope.$apply();
      expect(ctrl.title).toBe('title');
    });
  });
})();

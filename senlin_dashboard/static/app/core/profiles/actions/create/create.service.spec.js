/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
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

  describe('horizon.cluster.profiles.actions.create.service', function() {

    var model, service, $scope, workflow;
    var wizardModalService = {
      modal: function () {
        return {
          result: angular.noop
        };
      }
    };
    var senlinAPI = {
      createProfile: function(profile) {
        return {
          then: function(callback) {
            var newProfile = profile;
            newProfile.id = '1234';
            callback({data: profile});
          }
        };
      }
    };
    var profile = {name: 'test profile'};

    ///////////////////////

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster.profiles'));

    beforeEach(module(function($provide) {
      //$provide.value('horizon.cluster.profiles.actions.create.model', model);
      $provide.value('horizon.app.core.openstack-service-api.senlin', senlinAPI);
      $provide.value('horizon.framework.widgets.modal.wizard-modal.service', wizardModalService);
    }));

    beforeEach(inject(function($injector, _$rootScope_) {
      $scope = _$rootScope_.$new();
      model = $injector.get('horizon.cluster.profiles.actions.create.model');
      service = $injector.get('horizon.cluster.profiles.actions.create.service');
      workflow = $injector.get('horizon.cluster.profiles.actions.create.service.workflow');
    }));

    describe('perform', function() {
      it('open the modal with the correct parameters', function() {
        spyOn(wizardModalService, 'modal').and.callThrough();

        service.perform(profile, $scope);

        expect(wizardModalService.modal).toHaveBeenCalled();
        var modalArgs = wizardModalService.modal.calls.argsFor(0)[0];
        expect(modalArgs.scope).toEqual($scope);
        expect(modalArgs.workflow).toEqual(workflow);
        expect(modalArgs.submit).toBeDefined();
      });

      it('create profile', function() {
        var postProfile = { name: 'test', spec: 'spec', metadata: 'meta' };
        var newProfile = angular.copy(postProfile);
        newProfile.id = '1234';

        spyOn(senlinAPI, 'createProfile').and.callThrough();
        spyOn(wizardModalService, 'modal').and.callThrough();

        service.perform(profile, $scope);

        model.newProfileSpec = postProfile;

        var modalArgs = wizardModalService.modal.calls.argsFor(0)[0];
        modalArgs.submit();
        $scope.$apply();

        expect(senlinAPI.createProfile).toHaveBeenCalledWith(newProfile, true);
      });
    });

    describe('allowed', function() {
      it('should allow create profile', function() {
        var allowed = service.allowed();
        allowed.then(
          function() {
            expect(true).toBe(true);
          },
          function() {
            expect(false).toBe(true);
          });
        $scope.$apply();
      });
    });
  });
})();

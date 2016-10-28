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

  describe('horizon.cluster.profiles.actions.update.service', function() {

    var model, service, $scope, $q, workflow, policyAPI;
    var wizardModalService = {
      modal: function () {
        return {
          result: angular.noop
        };
      }
    };
    var senlinAPI = {
      getProfile: function() {
        return {
          then: function() {
            return { id: '1234' };
          }
        };
      },
      updateProfile: function(profile) {
        return {
          then: function(callback) {
            var newProfile = profile;
            newProfile.id = '1234';
            callback({data: profile});
          }
        };
      }
    };
    ///////////////////////

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster.profiles'));

    beforeEach(module(function($provide) {
      //$provide.value('horizon.cluster.profiles.actions.create.model', model);
      $provide.value('horizon.app.core.openstack-service-api.senlin', senlinAPI);
      $provide.value('horizon.framework.widgets.modal.wizard-modal.service', wizardModalService);
    }));

    beforeEach(inject(function($injector, _$rootScope_, _$q_) {
      $scope = _$rootScope_.$new();
      $q = _$q_;
      senlinAPI = $injector.get('horizon.app.core.openstack-service-api.senlin');
      policyAPI = $injector.get('horizon.app.core.openstack-service-api.policy');
      model = $injector.get('horizon.cluster.profiles.actions.create.model');
      service = $injector.get('horizon.cluster.profiles.actions.update.service');
      workflow = $injector.get('horizon.cluster.profiles.actions.update.service.workflow');
    }));

    describe('perform', function() {
      it('open the modal with the correct parameters', function() {
        var profile = {id: '1234', name: 'test profile'};
        spyOn(wizardModalService, 'modal').and.callThrough();
        spyOn(senlinAPI, 'getProfile').and.callThrough();

        service.perform(profile, $scope);
        expect(wizardModalService.modal).toHaveBeenCalled();

        var modalArgs = wizardModalService.modal.calls.argsFor(0)[0];
        expect(modalArgs.scope).toEqual($scope);
        expect(modalArgs.workflow).toEqual(workflow);
        expect(modalArgs.submit).toBeDefined();
      });

      it('update profile', function() {
        var postProfile = { id: '1234', name: 'test', spec: 'spec', metadata: 'meta' };
        var newProfile = angular.copy(postProfile);
        spyOn(senlinAPI, 'getProfile').and.callThrough();
        spyOn(senlinAPI, 'updateProfile').and.callThrough();
        spyOn(wizardModalService, 'modal').and.callThrough();

        service.perform(postProfile, $scope);

        model.newProfileSpec = postProfile;
        var modalArgs = wizardModalService.modal.calls.argsFor(0)[0];
        modalArgs.submit();
        $scope.$apply();

        expect(senlinAPI.updateProfile).toHaveBeenCalledWith(newProfile, true);
      });
    });

    describe('allowed', function() {
      it('should allow update profile', function() {
        var deferred = $q.defer();
        deferred.resolve(true);
        spyOn(policyAPI, 'ifAllowed').and.returnValue(deferred.promise);

        var allowed = service.allowed();

        expect(allowed).toBeTruthy();
        expect(policyAPI.ifAllowed).toHaveBeenCalledWith(
          { rules: [['cluster', 'profiles:update']] });
      });
    });
  });
})();

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

  describe('horizon.cluster.policies.actions.create.service', function() {

    var service, $scope, $q, deferred, senlin, workflow, $httpBackend;
    var model = {
      id: 1
    };
    var modal = {
      open: function (config) {
        config.model = model;
        deferred = $q.defer();
        deferred.resolve(config);
        return deferred.promise;
      }
    };

    ///////////////////

    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.cluster.policies'));

    beforeEach(module(function($provide) {
      $provide.value('horizon.framework.widgets.form.ModalFormService', modal);
    }));

    beforeEach(inject(function($injector, _$rootScope_, _$q_, _$httpBackend_) {
      $q = _$q_;
      $httpBackend = _$httpBackend_;
      $scope = _$rootScope_.$new();
      service = $injector.get('horizon.cluster.policies.actions.create.service');
      senlin = $injector.get('horizon.app.core.openstack-service-api.senlin');
      workflow = $injector.get('horizon.cluster.policies.actions.workflow');
      deferred = $q.defer();
      deferred.resolve({data: {id: 1}});
      spyOn(senlin, 'createPolicy').and.returnValue(deferred.promise);
      spyOn(modal, 'open').and.callThrough();
      spyOn(workflow, 'init').and.returnValue({model: model});
    }));

    it('should check the policy if the user is allowed to create policy', function() {
      var allowed = service.allowed();
      expect(allowed).toBeTruthy();
    });

    it('should initialize workflow and create profile', inject(function($timeout) {
      service.perform(model, $scope);

      expect(workflow.init).toHaveBeenCalled();

      var modalArgs = workflow.init.calls.mostRecent().args;
      expect(modalArgs[0]).toEqual('create');
      expect(modalArgs[1]).toEqual('Create Policy');
      expect(modalArgs[2]).toEqual('Create');

      expect(modal.open).toHaveBeenCalled();

      $httpBackend.expectGET('/static/app/core/policies/panel.html').respond({});
      $timeout.flush();
      $scope.$apply();

      expect(senlin.createPolicy).toHaveBeenCalled();
    }));
  });
})();

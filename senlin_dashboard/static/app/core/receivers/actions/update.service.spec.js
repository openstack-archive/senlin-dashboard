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

  describe('horizon.cluster.receivers.actions.update.service', function() {

    var service, $scope, $q, deferred, senlin;
    var selected = {
      id: 1
    };
    var model = {
      id: 1,
      name: ""
    };
    var modal = {
      open: function(config) {
        config.model = model;
        deferred = $q.defer();
        deferred.resolve(config);
        return deferred.promise;
      }
    };
    var workflow = {
      init: function (action, title) {
        action = title;
        return {model: model};
      }
    };

    ///////////////////

    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.cluster.receivers'));

    beforeEach(module(function($provide) {
      $provide.value('horizon.cluster.receivers.actions.workflow', workflow);
      $provide.value('horizon.framework.widgets.form.ModalFormService', modal);
    }));

    beforeEach(inject(function($injector, _$rootScope_, _$q_) {
      $q = _$q_;
      $scope = _$rootScope_.$new();
      service = $injector.get('horizon.cluster.receivers.actions.update.service');
      senlin = $injector.get('horizon.app.core.openstack-service-api.senlin');
      deferred = $q.defer();
      deferred.resolve({data: {id: 1}});
      spyOn(senlin, 'getReceiver').and.returnValue(deferred.promise);
      spyOn(senlin, 'updateReceiver').and.returnValue(deferred.promise);
      spyOn(workflow, 'init').and.callThrough();
      spyOn(modal, 'open').and.callThrough();
    }));

    it('should check the policy if the user is allowed to update Receiver', function() {
      var allowed = service.allowed();
      expect(allowed).toBeTruthy();
    });

    it('should initialize workflow and update Receiver', inject(function($timeout) {
      service.perform(selected, $scope);

      expect(workflow.init).toHaveBeenCalled();

      var modalArgs = workflow.init.calls.mostRecent().args;
      expect(modalArgs[0]).toEqual('update');
      expect(modalArgs[1]).toEqual('Update Receiver');
      expect(modalArgs[2]).toEqual('Update');

      expect(modal.open).toHaveBeenCalled();

      $timeout.flush();
      $scope.$apply();

      expect(senlin.updateReceiver).toHaveBeenCalled();
    }));
  });
})();

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

  describe('horizon.app.core.receivers.actions.delete.service', function() {

    var service, $scope, deferredModal;

    var deleteModalService = {
      open: function () {
        deferredModal.resolve({
          pass: [{context: {id: 'a'}}],
          fail: [{context: {id: 'b'}}]
        });
        return deferredModal.promise;
      }
    };

    var senlinAPI = {
      deleteReceiver: function() {
        return;
      }
    };

    var policyAPI = {
      ifAllowed: function() {
        return {
          success: function(callback) {
            callback({allowed: true});
          }
        };
      }
    };

    beforeEach(module('horizon.cluster.receivers'));

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core'));

    beforeEach(module('horizon.framework.widgets.modal', function($provide) {
      $provide.value('horizon.framework.widgets.modal.deleteModalService', deleteModalService);
    }));

    beforeEach(module('horizon.app.core.openstack-service-api', function($provide) {
      $provide.value('horizon.app.core.openstack-service-api.senlin', senlinAPI);
      $provide.value('horizon.app.core.openstack-service-api.policy', policyAPI);
      spyOn(policyAPI, 'ifAllowed').and.callThrough();
    }));

    beforeEach(inject(function($injector, _$rootScope_, $q) {
      $scope = _$rootScope_.$new();
      service = $injector.get('horizon.app.core.receivers.actions.delete.service');
      deferredModal = $q.defer();
    }));

    function generateReceivers(count) {
      var Receivers = [];
      var data = {
        name: 'delete_test',
        id: '1'
      };

      for (var index = 0; index < count; index++) {
        var receivers = angular.copy(data);
        receivers.id = index + 1;
        Receivers.push(receivers);
      }
      return Receivers;
    }

    describe('perform method', function() {

      beforeEach(function() {
        spyOn(deleteModalService, 'open').and.callThrough();
        service.initScope($scope, labelize);
      });

      function labelize(count) {
        return {
          title: ngettext('title', 'titles', count),
          message: ngettext('message', 'messages', count),
          submit: ngettext('submit', 'submits', count),
          success: ngettext('success', 'successes', count),
          error: ngettext('error', 'errors', count)
        };
      }

      it('should open the delete modal and show correct labels', testSingleObject);

      function testSingleObject() {
        var receivers = generateReceivers(1);
        service.perform(receivers[0]);
        $scope.$apply();

        expect(deleteModalService.open).toHaveBeenCalled();
      }

      it('should open the delete modal and show correct labels', testDoubleObject);

      function testDoubleObject() {
        var receivers = generateReceivers(2);
        service.perform(receivers);
        $scope.$apply();

        expect(deleteModalService.open).toHaveBeenCalled();
      }

      it('should pass in a function that deletes a receiver', testSenlin);

      function testSenlin() {
        spyOn(senlinAPI, 'deleteReceiver');
        var receivers = generateReceivers(1);
        var receiver = receivers[0];
        service.perform(receivers);
        $scope.$apply();

        var contextArg = deleteModalService.open.calls.argsFor(0)[2];
        var deleteFunction = contextArg.deleteEntity;
        deleteFunction(receiver.id);
      }
    });
  });
})();

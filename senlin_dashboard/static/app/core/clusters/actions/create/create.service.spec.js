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

  describe('horizon.cluster.clusters.actions.create.service', function() {

    var service, $scope, $q, modal, basePath, workflow, senlinAPI, policyAPI;
    var createClusterResponse = {
      data: {
        id: "9874",
        name: "test_cluster",
        profile_id: "1234",
        min_size: 0,
        max_size: -1,
        desired_capacity: 0,
        timeout: 0,
        metadata: ""
      }
    };

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster'));
    beforeEach(module('horizon.cluster.clusters.actions'));

    beforeEach(inject(function($injector, _$rootScope_, _$q_) {
      $scope = _$rootScope_.$new();
      $q = _$q_;

      senlinAPI = $injector.get('horizon.app.core.openstack-service-api.senlin');
      policyAPI = $injector.get('horizon.app.core.openstack-service-api.policy');
      modal = $injector.get('horizon.framework.widgets.form.ModalFormService');
      basePath = $injector.get('horizon.app.core.clusters.basePath');
      workflow = $injector.get('horizon.cluster.clusters.actions.workflow');
      service = $injector.get('horizon.cluster.clusters.actions.create.service');
    }));

    describe('should defined a model and initialized', function() {
      it('open the modal', function() {
        var deferred = $q.defer();
        deferred.resolve(true);
        spyOn(modal, "open").and.returnValue($q.defer().promise);

        var deferredGetProfiles = $q.defer();
        deferredGetProfiles.resolve(createClusterResponse);
        spyOn(senlinAPI, 'getProfiles').and.returnValue(deferredGetProfiles.promise);

        spyOn(workflow, 'init').and.callThrough();

        service.perform();
        $scope.$apply();

        expect(workflow.init).toHaveBeenCalled();

        var modalArgs = workflow.init.calls.mostRecent().args;
        expect(modalArgs[0]).toEqual('create');
        expect(modalArgs[1]).toEqual('Create Cluster');
        expect(modalArgs[2]).toEqual('Create');
        expect(modalArgs[3]).toEqual(basePath + 'actions/create/cluster.help.html');

        expect(modal.open).toHaveBeenCalled();
      });
    });

    describe('allowed', function() {
      it('should allow create cluster', function() {
        var deferred = $q.defer();
        deferred.resolve(true);
        spyOn(policyAPI, 'ifAllowed').and.returnValue(deferred.promise);

        var allowed = service.allowed();

        expect(allowed).toBeTruthy();
        expect(policyAPI.ifAllowed).toHaveBeenCalledWith(
          { rules: [['cluster', 'clusters:create']] });
      });
    });
  });
})();

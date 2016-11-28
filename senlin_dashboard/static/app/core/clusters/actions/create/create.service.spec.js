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

    var service, $scope, $q, modal, senlinAPI, policyAPI;
    var createClusterResponse = {
      data: {
        name: "test_cluster",
        profile_id: "1234",
        min_size: 0,
        max_size: -1,
        desired_capacity: 0,
        timeout: 0,
        metadata: ""
      }
    };

    var getProfilesResponse = {
      data: {
        items: [
          {
            name: 'test_profile',
            id: '5678'
          }
        ]
      }
    };

    beforeEach(module('horizon.framework'));
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster.clusters.actions'));

    beforeEach(inject(function($injector, _$rootScope_, _$q_) {
      $scope = _$rootScope_.$new();
      $q = _$q_;

      senlinAPI = $injector.get('horizon.app.core.openstack-service-api.senlin');
      policyAPI = $injector.get('horizon.app.core.openstack-service-api.policy');
      modal = $injector.get('horizon.framework.widgets.form.ModalFormService');
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

        service.initAction();
        service.perform();
        $scope.$apply();

        expect(modal.open).toHaveBeenCalled();
        expect(service.getModel(), createClusterResponse.data);
      });

      it('should call senlin.createCluster', function() {
        var deferred = $q.defer();
        deferred.resolve(true);
        spyOn(modal, "open").and.returnValue(deferred.promise);

        var deferredCreateCluster = $q.defer();
        deferredCreateCluster.resolve(createClusterResponse);
        spyOn(senlinAPI, 'createCluster').and.returnValue(deferredCreateCluster.promise);

        service.perform();
        $scope.$apply();

        expect(senlinAPI.createCluster).toHaveBeenCalled();
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

/*
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function() {
  "use strict";

  describe('Cluster service', function() {
    var service, $scope, detailRoute;
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster'));

    beforeEach(inject(function($injector, _$rootScope_) {
      service = $injector.get('horizon.cluster.clusters.service');
      detailRoute = $injector.get('horizon.app.core.detailRoute');
      $scope = _$rootScope_.$new();
    }));

    it("getDetailsClusterPath creates urls using the item's ID", function() {
      var myItem = {id: "666"};
      expect(service.getDetailsClusterPath(myItem)).toBe(
        detailRoute + 'OS::Senlin::Cluster/666');
    });

    it("getDetailsProfilePath creates urls using the item's ID", function() {
      var myItem = {profile_id: "666"};
      expect(service.getDetailsProfilePath(myItem)).toBe(
        detailRoute + 'OS::Senlin::Profile/666');
    });

    describe('getClusterPromise', function() {
      it("get cluster promise", inject(function($q, $injector) {
        var senlin = $injector.get('horizon.app.core.openstack-service-api.senlin');
        var deferred = $q.defer();
        spyOn(senlin, 'getCluster').and.returnValue(deferred.promise);
        var result = service.getClusterPromise({});
        deferred.resolve({id: 1, name: 'test-cluster'});
        $scope.$apply();
        expect(result.$$state.value.id).toBe(1);
      }));
    });

    describe('getClustersPromise', function() {
      it("get clusters promise", inject(function($q, $injector) {
        var senlin = $injector.get('horizon.app.core.openstack-service-api.senlin');
        var deferred = $q.defer();
        spyOn(senlin, 'getClusters').and.returnValue(deferred.promise);
        var result = service.getClustersPromise({});
        deferred.resolve({data: {items: [{id: 1, name: 'test-cluster'}]}});
        $scope.$apply();
        expect(result.$$state.value.data.items[0].name).toBe('test-cluster');
      }));
    });
  });

})();

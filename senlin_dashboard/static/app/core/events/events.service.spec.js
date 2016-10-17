/*
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

  describe('node service', function() {
    var service, $scope;
    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.cluster'));

    beforeEach(inject(function($injector, _$rootScope_) {
      service = $injector.get('horizon.cluster.events.service');
      $scope = _$rootScope_.$new();
    }));

    describe('getEventsPromise', function() {
      it("get events promise", inject(function($q, $injector) {
        var senlin = $injector.get('horizon.app.core.openstack-service-api.senlin');
        var deferred = $q.defer();
        spyOn(senlin, 'getEvents').and.returnValue(deferred.promise);
        var result = service.getEventsPromise({obj_id: 666});
        deferred.resolve({data: {items: [{id: 1, name: 'test-node'}]}});
        $scope.$apply();
        expect(result.$$state.value.data.items[0].name).toBe('test-node');
      }));
    });
  });

})();

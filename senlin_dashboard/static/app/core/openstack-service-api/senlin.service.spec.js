/**
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
  'use strict';

  describe('Senlin API', function() {
    var testCall, service;
    var apiService = {};
    var toastService = {};

    beforeEach(
      module('horizon.mock.openstack-service-api',
        function($provide, initServices) {
          testCall = initServices($provide, apiService, toastService);
        })
    );

    beforeEach(module('horizon.app.core.openstack-service-api'));

    beforeEach(inject(['horizon.app.core.openstack-service-api.senlin', function(senlinAPI) {
      service = senlinAPI;
    }]));

    it('defines the service', function() {
      expect(service).toBeDefined();
    });

    var tests = [
      {
        func: 'getReceivers',
        method: 'get',
        path: '/api/senlin/receivers/',
        data: { params: 'config' },
        error: 'Unable to retrieve the receivers.',
        testInput: [ 'config' ]
      },
      {
        func: 'getReceiver',
        method: 'get',
        path: '/api/senlin/receivers/666/',
        error: 'Unable to retrieve the receiver with id: 666.',
        testInput: [666]
      },
      {
        func: 'deleteReceiver',
        method: 'delete',
        path: '/api/senlin/receivers/666/',
        error: 'Unable to delete the receiver with id: 666.',
        testInput: [666]
      },
      {
        func: 'getProfiles',
        method: 'get',
        path: '/api/senlin/profiles/',
        data: { params: 'config' },
        error: 'Unable to retrieve the profiles.',
        testInput: [ 'config' ]
      },
      {
        func: 'getProfile',
        method: 'get',
        path: '/api/senlin/profiles/666/',
        error: 'Unable to retrieve the profile with id: 666.',
        testInput: [666]
      },
      {
        func: 'deleteProfile',
        method: 'delete',
        path: '/api/senlin/profiles/666/',
        error: 'Unable to delete the profile with id: 666.',
        testInput: [666]
      },
      {
        func: 'deleteCluster',
        method: 'delete',
        path: '/api/senlin/clusters/666/',
        error: 'Unable to delete the cluster with id: 666.',
        testInput: [666]
      },
      {
        func: 'getNodes',
        method: 'get',
        path: '/api/senlin/nodes/',
        data: { params: 'config' },
        error: 'Unable to retrieve the nodes.',
        testInput: [ 'config' ]
      },
      {
        func: 'getNode',
        method: 'get',
        path: '/api/senlin/nodes/666/',
        error: 'Unable to retrieve the node with id: 666.',
        testInput: [666]
      },
      {
        func: 'getEvents',
        method: 'get',
        path: '/api/senlin/events/666/',
        error: 'Unable to retrieve the events with id: 666.',
        testInput: [666]
      },
      {
        func: 'getPolicies',
        method: 'get',
        path: '/api/senlin/policies/',
        data: { params: 'config' },
        error: 'Unable to retrieve the policies.',
        testInput: [ 'config' ]
      },
      {
        func: 'getPolicy',
        method: 'get',
        path: '/api/senlin/policies/666/',
        error: 'Unable to retrieve the policy with id: 666.',
        testInput: [666]
      },
      {
        func: 'deletePolicy',
        method: 'delete',
        path: '/api/senlin/policies/666/',
        error: 'Unable to delete the policy with id: 666.',
        testInput: [666]
      }
    ];

    // Iterate through the defined tests and apply as Jasmine specs.
    angular.forEach(tests, function(params) {
      it('defines the ' + params.func + ' call properly', function() {
        var callParams = [apiService, service, toastService, params];
        testCall.apply(this, callParams);
      });
    });

    it('supresses the error if instructed for deleteReceiver', function() {
      spyOn(apiService, 'delete').and.returnValue("promise");
      expect(service.deleteReceiver("whatever", true)).toBe("promise");
    });

    it('supresses the error if instructed for deleteProfile', function() {
      spyOn(apiService, 'delete').and.returnValue("promise");
      expect(service.deleteProfile("whatever", true)).toBe("promise");
    });

    it('supresses the error if instructed for deleteCluster', function() {
      spyOn(apiService, 'delete').and.returnValue("promise");
      expect(service.deleteCluster("whatever", true)).toBe("promise");
    });

    it('supresses the error if instructed for deletePolicy', function() {
      spyOn(apiService, 'delete').and.returnValue("promise");
      expect(service.deletePolicy("whatever", true)).toBe("promise");
    });

  });

})();

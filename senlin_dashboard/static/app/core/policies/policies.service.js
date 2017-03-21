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

  angular
    .module('horizon.cluster.policies')
    .factory('horizon.cluster.policies.service', policiesService);

  policiesService.$inject = [
    'horizon.app.core.detailRoute',
    'horizon.app.core.openstack-service-api.senlin'
  ];

  /*
   * @ngdoc factory
   * @name horizon.cluster.policies.service
   *
   * @description
   * This service provides functions that are used through
   * the policies features.
   */
  function policiesService(detailRoute, senlin) {
    return {
      getDetailsPath: getDetailsPath,
      getPolicyPromise: getPolicyPromise,
      getPoliciesPromise: getPoliciesPromise
    };

    /*
     * @ngdoc function
     * @name getDetailsPath
     * @param item {Object} - The policy object
     * @description
     * Returns the relative path to the details view.
     */
    function getDetailsPath(item) {
      return detailRoute + 'OS::Senlin::Policy/' + item.id;
    }

    /*
     * @ngdoc function
     * @name getPolicyPromise
     * @description
     * Given an id, returns a promise for the policy data.
     */
    function getPolicyPromise(identifier) {
      return senlin.getPolicy(identifier);
    }

    /*
     * @ngdoc function
     * @name getPoliciesPromise
     * @description
     * Given filter/query parameters, returns a promise for the matching
     * policies.  This is used in displaying lists of Policies.
     */
    function getPoliciesPromise(params) {
      return senlin.getPolicies(params).then(modifyResponse);
    }

    function modifyResponse(response) {
      return {data: {items: response.data.items.map(modifyItem)}};

      function modifyItem(item) {
        var timestamp = item.updated_at ? item.updated_at : item.created_at;
        item.trackBy = item.id + timestamp;
        return item;
      }
    }
  }
})();

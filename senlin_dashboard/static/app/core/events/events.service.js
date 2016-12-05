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
    .module('horizon.cluster.events')
    .factory('horizon.cluster.events.service', eventsService);

  eventsService.$inject = [
    'horizon.app.core.openstack-service-api.senlin'
  ];

  /*
   * @ngdoc factory
   * @name horizon.cluster.events.service
   *
   * @description
   * This service provides functions that are used through
   * the Events features.
   */
  function eventsService(senlin) {
    return {
      getEventsPromise: getEventsPromise
    };

    /*
     * @ngdoc function
     * @name getEventsPromise
     * @description
     * Given object ID, returns a promise for the matching events.
     * This is used in displaying lists of Events.
     */
    function getEventsPromise(params) {
      return senlin.getEvents(params.obj_id);
    }
  }
})();

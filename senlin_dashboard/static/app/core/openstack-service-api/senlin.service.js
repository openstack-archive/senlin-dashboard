/**
 * Copyright 2015 IBM Corp.
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
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.senlin', senlinAPI);

  senlinAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'
  ];

  /**
   * @ngdoc service
   * @param {Object} apiService
   * @param {Object} toastService
   * @name senlin
   * @description Provides direct access to Senlin APIs.
   * @returns {Object} The service
   */
  function senlinAPI(apiService, toastService) {
    var service = {
      getReceivers: getReceivers,
      getReceiver: getReceiver,
      deleteReceiver: deleteReceiver
    };

    return service;

    ///////////////

    // Receivers

    /*
     * @name getReceivers
     * @description
     * Get a list of receivers.
     */
    function getReceivers(params) {
      var config = params ? {params: params} : {};
      return apiService.get('/api/senlin/receivers/', config)
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the receivers.'));
        });
    }

    /*
     * @name getReceiver
     * @description
     * Get a single receiver by ID
     *
     * @param {string} id
     * Specifies the id of the receiver to request.
     *
     * @returns {Object} The result of the API call
     */
    function getReceiver(id) {
      return apiService.get('/api/senlin/receivers/' + id + '/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the receiver.'));
        });
    }

    /**
     * @name deleteReceiver
     * @description
     * Deletes single Receiver by ID.
     *
     * @param {string} receiverId
     * The Id of the receiver to delete.
     *
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     *
     * @returns {Object} The result of the API call
     */
    function deleteReceiver(receiverId, suppressError) {
      var promise = apiService.delete('/api/senlin/receivers/' + receiverId + '/');

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the receiver with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: receiverId }, true));
      });
    }

  }
}());

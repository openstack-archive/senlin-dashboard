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
      createCluster: createCluster,
      updateCluster: updateCluster,
      deleteCluster: deleteCluster,
      scaleCluster: scaleCluster,
      resizeCluster: resizeCluster,
      createProfile: createProfile,
      updateProfile: updateProfile,
      deleteProfile: deleteProfile,
      getProfiles: getProfiles,
      getProfile: getProfile,
      getNodes: getNodes,
      getNode: getNode,
      createNode: createNode,
      updateNode: updateNode,
      deleteNode: deleteNode,
      getEvents: getEvents,
      getReceivers: getReceivers,
      getReceiver: getReceiver,
      createReceiver: createReceiver,
      updateReceiver: updateReceiver,
      deleteReceiver: deleteReceiver,
      getCluster: getCluster,
      getClusters: getClusters,
      getPolicy: getPolicy,
      getPolicies: getPolicies,
      createPolicy: createPolicy,
      updatePolicy: updatePolicy,
      deletePolicy: deletePolicy,
      getClusterPolicies: getClusterPolicies,
      updateClusterPolicies: updateClusterPolicies
    };

    return service;

    ///////////////

    // Nodes

    /**
     * @name getNodes
     * @description
     * Get a list of nodes.
     *
     * @param {string} params
     * The Id of the profile to delete.
     *
     * @returns {Object} The result of the API call
     */
    function getNodes(params) {
      var config = params ? {params: params} : {};
      return apiService.get('/api/senlin/nodes/', config)
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the nodes.'));
        });
    }

    /**
     * @name getNode
     * @description
     * Get a list of node.
     *
     * @param {string} id
     * The Id of the node to get.
     *
     * @returns {Object} The result of the API call
     */
    function getNode(id) {
      return apiService.get('/api/senlin/nodes/' + id + '/')
        .error(function () {
          var msg = gettext('Unable to retrieve the node with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    /**
     * @name createNode
     * @description
     * Create new Node.
     *
     * @param {Object} params
     * JSON object to create new node like name, profile_id, cluster_id, role
     * and metadata.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function createNode(params, suppressError) {
      var promise = apiService.post('/api/senlin/nodes/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to create the node with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
      * @name updateNode
      * @description
      * Update a Node.
      *
      * @param {Object} id
      * Node ID to update.
      * @param {Object} params
      * JSON object to update a node like name, profile_id, cluster_id, role
      * and metadata.
      * @param {boolean} suppressError
      * If passed in, this will not show the default error handling
      * @returns {Object} The result of the API call
      */
    function updateNode(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/nodes/' + id + '/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to update the node with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
     * @name deleteNode
     * @description
     * Deletes single Node by ID.
     *
     * @param {string} nodeId
     * The Id of the node to delete.
     *
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     *
     * @returns {Object} The result of the API call
     */
    function deleteNode(nodeId, suppressError) {
      var promise = apiService.delete('/api/senlin/nodes/' + nodeId + '/');

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the node with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: nodeId }, true));
      });
    }

    // Events

    /**
     * @name getEvents
     * @description
     * Get a list of events.
     *
     * @param {string} objId
     * The Id of the object to get events.
     *
     * @returns {Object} The result of the API call
     */
    function getEvents(objId) {
      return apiService.get('/api/senlin/events/' + objId + '/')
        .error(function () {
          var msg = gettext('Unable to retrieve the events with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: objId}, true));
        });
    }

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
          var msg = gettext('Unable to retrieve the receiver with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    /**
     * @name createReceiver
     * @description
     * Create new Receiver.
     *
     * @param {Object} params
     * JSON object to create new receiver like name, type, cluster_id, action
     * and params.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function createReceiver(params, suppressError) {
      var promise = apiService.post('/api/senlin/receivers/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to create the receiver with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
     * @name updateReceiver
     * @description
     * Update a Receiver.
     *
     * @param {Object} id
     * Receiver ID to update.
     * @param {Object} params
     * JSON object to update a receiver like name, action and param.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function updateReceiver(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/receivers/' + id + '/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to update the receiver with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
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
        var msg = gettext('Unable to delete the receiver with id: %(id)s.');
        toastService.add('error', interpolate(msg, { id: receiverId }, true));
      });
    }

    // Profiles

    /*
     * @name getProfiles
     * @description
     * Get a list of profiles.
     */
    function getProfiles(params) {
      var config = params ? {params: params} : {};
      return apiService.get('/api/senlin/profiles/', config)
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the profiles.'));
        });
    }

    /*
     * @name getProfile
     * @description
     * Get a list of profile.
     */
    function getProfile(id) {
      return apiService.get('/api/senlin/profiles/' + id + '/')
        .error(function () {
          var msg = gettext('Unable to retrieve the profile with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    /**
     * @name deleteProfile
     * @description
     * Deletes single Profile by ID.
     *
     * @param {string} profileId
     * The Id of the profile to delete.
     *
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     *
     * @returns {Object} The result of the API call
     */
    function deleteProfile(profileId, suppressError) {
      var promise = apiService.delete('/api/senlin/profiles/' + profileId + '/');

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the profile with id: %(id)s.');
        toastService.add('error', interpolate(msg, { id: profileId }, true));
      });
    }

    /**
     * @name createProfile
     * @description
     * Create new Profile.
     *
     * @param {Object} params
     * JSON object to create new profile like name, spec, metadata.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function createProfile(params, suppressError) {
      var promise = apiService.post('/api/senlin/profiles/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to create the profile with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

   /**
     * @name updateProfile
     * @description
     * Update a Profile.
     *
     * @param {Object} id
     * @param {Object} params
     * JSON object to update a profile like name, metadata.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function updateProfile(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/profiles/' + id + '/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to update the profile with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    // Clusters

    /*
     * @name getClusters
     * @description
     * Get a list of clusters.
     */
    function getClusters(params) {
      var config = params ? {params: params} : {};
      return apiService.get('/api/senlin/clusters/', config)
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the clusters.'));
        });
    }

    /*
     * @name getCluster
     * @description
     * Get a single cluster by ID.
     */
    function getCluster(id) {
      return apiService.get('/api/senlin/clusters/' + id + '/')
        .error(function () {
          var msg = gettext('Unable to retrieve the cluster with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    ///// cluster

    /**
     * @name createCluster
     * @description
     * Create new Cluster.
     *
     * @param {Object} params
     * JSON object to create new cluster like name, metadata.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function createCluster(params, suppressError) {
      var promise = apiService.post('/api/senlin/clusters/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to create the cluster with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
      * @name updateCluster
      * @description
      * Update a Cluster.
      *
      * @param {Object} id
      * Cluster ID to update.
      * @param {Object} params
      * JSON object to update a cluster like name.
      * @param {boolean} suppressError
      * If passed in, this will not show the default error handling
      * @returns {Object} The result of the API call
      */
    function updateCluster(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/clusters/' + id + '/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to update the cluster with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
     * @name deleteCluster
     * @description
     * Deletes single Cluster by ID.
     *
     * @param {string} clusterId
     * The Id of the cluster to delete.
     *
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     *
     * @returns {Object} The result of the API call
     */
    function deleteCluster(clusterId, suppressError) {
      var promise = apiService.delete('/api/senlin/clusters/' + clusterId + '/');

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the cluster with id: %(id)s.');
        toastService.add('error', interpolate(msg, { id: clusterId }, true));
      });
    }

    /**
     * @name scaleCluster
     * @description
     * Scale a Cluster.
     *
     * @param {Object} id
     * Cluster ID to scale.
     * @param {Object} name
     * Cluster name to scale.
     * @param {Object} scale
     * Direction of scale. 'in' or 'out'.
     * @param {Object} count
     * Count to scale-in a cluster.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function scaleCluster(id, name, scale, count, suppressError) {
      var promise = apiService.put(
        '/api/senlin/clusters/' + id + '/scale-' + scale,
        {count: count});

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to scale-%(scale)s the cluster with name: %(name)s');
        var scaleMsg;
        if (scale === 'in') {
          scaleMsg = gettext('in');
        } else {
          scaleMsg = gettext('out');
        }
        toastService.add('error', interpolate(msg, { scale: scaleMsg, name: name }, true));
      });
    }

    /**
     * @name resizeCluster
     * @description
     * Scale a Cluster.
     *
     * @param {Object} id
     * Cluster ID to scale.
     * @param {Object} name
     * Cluster name to scale.
     * @param {Object} params
     * Parameters to resize.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function resizeCluster(id, name, params, suppressError) {
      var promise = apiService.put(
        '/api/senlin/clusters/' + id + '/resize', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to resize the cluster with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: name }, true));
      });
    }

    /*
     * @name getClusterPolicies
     * @description
     * Get policies of a single cluster by ID.
     */
    function getClusterPolicies(id) {
      return apiService.get('/api/senlin/clusters/' + id + '/policy')
        .error(function () {
          var msg = gettext('Unable to retrieve the policies of the cluster with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    /**
     * @name updateClusterPolicies
     * @description
     * Update policies for the cluster
     *
     * @param {String} id
     * ID of the cluster to be updated
     * @param {Object} params
     * JSON object to attach policies.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function updateClusterPolicies(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/clusters/' + id + '/policy' , params);
      return suppressError ? promise : promise.error(function() {
        toastService.add('error', gettext('Unable to update policies of the cluster'));
      });
    }

    // Policies

    /*
     * @name getPolicies
     * @description
     * Get a list of policies.
     */
    function getPolicies(params) {
      var config = params ? {params: params} : {};
      return apiService.get('/api/senlin/policies/', config)
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve the policies.'));
        });
    }

    /*
     * @name getPolicy
     * @description
     * Get a single policy by ID.
     */
    function getPolicy(id) {
      return apiService.get('/api/senlin/policies/' + id + '/')
        .error(function () {
          var msg = gettext('Unable to retrieve the policy with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    /**
     * @name createPolicy
     * @description
     * Create new Policy.
     *
     * @param {Object} params
     * JSON object to create new policy like name and spec.
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     * @returns {Object} The result of the API call
     */
    function createPolicy(params, suppressError) {
      var promise = apiService.post('/api/senlin/policies/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to create the policy with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
      * @name updatePolicy
      * @description
      * Update a Policy.
      *
      * @param {Object} id
      * Policy ID to update.
      * @param {Object} params
      * JSON object to update a policy like name.
      * @param {boolean} suppressError
      * If passed in, this will not show the default error handling
      * @returns {Object} The result of the API call
      */
    function updatePolicy(id, params, suppressError) {
      var promise = apiService.put('/api/senlin/policies/' + id + '/', params);

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to update the policy with name: %(name)s');
        toastService.add('error', interpolate(msg, { name: params.name }, true));
      });
    }

    /**
     * @name deletePolicy
     * @description
     * Deletes single Policy by ID.
     *
     * @param {string} policyId
     * The Id of the policy to delete.
     *
     * @param {boolean} suppressError
     * If passed in, this will not show the default error handling
     *
     * @returns {Object} The result of the API call
     */
    function deletePolicy(policyId, suppressError) {
      var promise = apiService.delete('/api/senlin/policies/' + policyId + '/');

      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the policy with id: %(id)s.');
        toastService.add('error', interpolate(msg, { id: policyId }, true));
      });
    }
  }
})();

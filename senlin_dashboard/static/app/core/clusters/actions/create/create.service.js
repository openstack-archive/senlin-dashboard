/**
 * Copyright 2016 NEC Corporation
 *
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

  /**
   * @ngdoc factory
   * @name horizon.cluster.clusters.actions.create.service
   * @description
   * Service for the cluster cluster create modal
   */
  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.create.service', createService);

  createService.$inject = [
    '$location',
    'horizon.app.core.clusters.basePath',
    'horizon.app.core.clusters.resourceType',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service'
  ];

  function createService($location, path, resourceType, policy, senlin, gettext,
    actionResult, modalFormService, toast
  ) {
    var model;
    var profiles = [{name: gettext('Select Profile'), value: ''}];
    var schema = {
      type: 'object',
      properties: {
        name: {
          title: gettext('Cluster Name'),
          type: 'string'
        },
        profile_id: {
          title: gettext('Profile'),
          type: 'string'
        },
        min_size: {
          title: gettext('Min Size'),
          type: 'integer'
        },
        max_size: {
          title: gettext('Max Size'),
          type: 'integer'
        },
        desired_capacity: {
          title: gettext('Desired Capacity'),
          type: 'integer'
        },
        timeout: {
          title: gettext('Timeout'),
          type: 'integer'
        },
        metadata: {
          title: gettext('Metadata'),
          type: 'string'
        }
      },
      required: ['name', 'profile_id', 'desired_capacity']
    };

    var form = [
      {
        type: 'section',
        htmlClass: 'row',
        items: [
          {
            type: 'section',
            htmlClass: 'col-sm-6',
            items: [
              {
                key: 'name'
              },
              {
                key: 'profile_id',
                type: 'select',
                titleMap: profiles
              },
              'min_size',
              'max_size',
              'desired_capacity',
              'timeout',
              {
                key: 'metadata',
                type: 'textarea'
              }
            ]
          },
          {
            type: 'template',
            templateUrl: path + 'actions/create/cluster.help.html'
          }
        ]
      }
    ];

    var service = {
      initAction: initAction,
      allowed: allowed,
      perform: perform,
      getModel: getModel
    };

    return service;

    //////////////

    function initAction() {
      senlin.getProfiles().then(onGetProfiles);
    }

    function onGetProfiles(response) {
      angular.forEach(response.data.items, function(item) {
        profiles.push({value: item.id, name: item.name});
      });
    }

    function initModel() {
      model = {
        name: "",
        profile_id: "",
        min_size: 0,
        max_size: -1,
        desired_capacity: 0,
        timeout: 0,
        metadata: ""
      };
    }

    function getModel() {
      return model;
    }

    function allowed() {
      return policy.ifAllowed({ rules: [['cluster', 'clusters:create']] });
    }

    function onSubmit() {
      return senlin.createCluster(model, false).then(success, true);
    }

    function success(response) {
      var message = gettext('Cluster %s was successfully created.');
      toast.add('success', interpolate(message, [response.data.id]));
      var result = actionResult.getActionResult()
                   .created(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.created.length > 0) {
        $location.path("/cluster");
      } else {
        return result.result;
      }
    }

    function perform() {
      initModel();
      var config = {
        title: gettext("Create Cluster"),
        schema: schema,
        form: form,
        model: model
      };
      return modalFormService.open(config).then(onSubmit);
    }
  }
})();

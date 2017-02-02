/**
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
   * @name horizon.cluster.clusters.actions.workflow
   * @ngController
   *
   * @description
   * Workflow for creating/updating cluster cluster
   */
  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.workflow', workflow);

  workflow.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.i18n.gettext'
  ];

  function workflow(senlin, gettext) {
    var workflow = {
      init: init
    };

    function init(actionType, title, submitText, helpUrl) {
      var schema, form, model;

      // schema
      schema = {
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
        }
      };

      // form
      form = [
        {
          type: 'section',
          htmlClass: 'row',
          items: [
            {
              type: 'section',
              htmlClass: 'col-sm-6',
              items: [
                {
                  key: 'name',
                  placeholder: gettext('Name of the cluster.'),
                  required: true
                },
                {
                  key: 'profile_id',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select profile for the cluster.')}
                  ],
                  required: true
                },
                {
                  key: 'min_size',
                  readonly: actionType === 'update'
                },
                {
                  key: 'max_size',
                  readonly: actionType === 'update'
                },
                {
                  key: 'desired_capacity',
                  required: actionType === 'create',
                  readonly: actionType === 'update'
                },
                {
                  key: 'timeout'
                },
                {
                  key: 'metadata',
                  type: 'textarea',
                  placeholder: gettext('Metadata of the cluster in YAML format.')
                }
              ]
            },
            {
              type: 'template',
              templateUrl: helpUrl
            }
          ]
        }
      ]; // form

      // Get profiles
      senlin.getProfiles().then(onGetProfiles);
      function onGetProfiles(response) {
        angular.forEach(response.data.items, function(item) {
          form[0].items[0].items[1].titleMap.push({value: item.id, name: item.name});
        });
      }

      model = {
        id: '',
        name: '',
        profile_id: '',
        min_size: 0,
        max_size: -1,
        desired_capacity: 0,
        timeout: 0,
        metadata: ''
      };

      var config = {
        title: title,
        submitText: submitText,
        schema: schema,
        form: form,
        model: model
      };

      return config;
    }

    return workflow;
  }
})();

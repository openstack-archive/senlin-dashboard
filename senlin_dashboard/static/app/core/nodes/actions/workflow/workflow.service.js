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
   * @name horizon.cluster.nodes.actions.workflow
   * @ngController
   *
   * @description
   * Workflow for creating/updating cluster node
   */
  angular
    .module('horizon.cluster.nodes.actions')
    .factory('horizon.cluster.nodes.actions.workflow', workflow);

  workflow.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.framework.util.i18n.gettext'
  ];

  function workflow(senlin, gettext) {
    var workflow = {
      init: init
    };

    function init(actionType, title, submitText, submitIcon, helpUrl) {
      var schema, form, model;

      // schema
      schema = {
        type: 'object',
        properties: {
          name: {
            title: gettext('Name'),
            type: 'string'
          },
          profile_id: {
            title: gettext('Profile'),
            type: 'string',
            default: ''
          },
          cluster_id: {
            title: gettext('Cluster'),
            type: 'string',
            default: ''
          },
          role: {
            title: gettext('Role'),
            type: 'string'
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
                  placeholder: gettext('Name of the node.'),
                  required: true
                },
                {
                  key: 'profile_id',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select profile for the node.')}
                  ],
                  required: actionType === 'create'
                },
                {
                  key: 'cluster_id',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select cluster for the node.')}
                  ],
                  readonly: actionType === 'update'
                },
                {
                  key: 'role',
                  placeholder: gettext('Role for this node in the cluster.')
                },
                {
                  key: 'metadata',
                  type: 'textarea',
                  placeholder: gettext('Metadata of the node in YAML format.')
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
      // Get clusters
      senlin.getClusters().then(onGetClusters);
      function onGetClusters(response) {
        angular.forEach(response.data.items, function(item) {
          form[0].items[0].items[2].titleMap.push({value: item.id, name: item.name});
        });
      }

      model = {
        id: '',
        name: '',
        profile_id: '',
        cluster_id: '',
        role: '',
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

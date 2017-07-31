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
   * @name horizon.cluster.receivers.actions.workflow
   * @ngController
   *
   * @description
   * Workflow for creating/updating receiver
   */
  angular
    .module('horizon.cluster.receivers.actions')
    .factory('horizon.cluster.receivers.actions.workflow', workflow);

  workflow.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.receivers.basePath',
    'horizon.framework.util.i18n.gettext'
  ];

  function workflow(senlin, basePath, gettext) {
    var workflow = {
      init: init
    };

    function init(actionType, title, submitText) {
      var schema, form, model;
      var helpUrl = basePath + 'actions/receiver.help.html';

      // schema
      schema = {
        type: 'object',
        properties: {
          name: {
            title: gettext('Name'),
            type: 'string'
          },
          type: {
            title: gettext('Type'),
            type: 'string',
            default: ''
          },
          cluster_id: {
            title: gettext('Cluster'),
            type: 'string',
            default: ''
          },
          action: {
            title: gettext('Action'),
            type: 'string'
          },
          params: {
            title: gettext('Params'),
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
                  placeholder: gettext('Name of the receiver.'),
                  required: true
                },
                {
                  key: 'type',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select type for the receiver.')},
                    {value: 'webhook', name: gettext('Webhook')},
                    {value: 'message', name: gettext('Message')}
                  ],
                  required: true,
                  readonly: actionType === 'update'
                },
                {
                  key: 'cluster_id',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select cluster for the receiver.')}
                  ],
                  required: "model.type === 'webhook' || model.type === ''",
                  readonly: actionType === 'update'
                },
                {
                  key: 'action',
                  type: 'select',
                  titleMap: [
                    {value: '', name: gettext('Select action for the receiver.')},
                    {value: 'CLUSTER_SCALE_IN', name: gettext('Scale In the Cluster')},
                    {value: 'CLUSTER_SCALE_OUT', name: gettext('Scale Out the Cluster')}
                  ],
                  required: "model.type === 'webhook' || model.type === ''"
                },
                {
                  key: 'params',
                  type: 'textarea',
                  placeholder: gettext('Parameters of the receiver in YAML format.')
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
        type: '',
        cluster_id: '',
        action: '',
        params: ''
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

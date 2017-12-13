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
   * @name horizon.cluster.policies.actions.workflow
   * @ngController
   *
   * @description
   * Workflow for creating/updating cluster policy
   */
  angular
    .module('horizon.cluster.policies.actions')
    .factory('horizon.cluster.policies.actions.workflow', workflow);

  workflow.$inject = [
    'horizon.app.core.policies.basePath',
    'horizon.framework.util.i18n.gettext'
  ];

  function workflow(basePath, gettext) {
    var workflow = {
      init: init
    };

    function init(actionType, title, submitText, scope) {
      var schema, form, model;

      // schema
      schema = {
        type: 'object',
        properties: {
          name: {
            title: gettext('Name'),
            type: 'string'
          },
          spec: {
            title: gettext('Spec'),
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
                  placeholder: gettext('Name of the policy.'),
                  required: true
                },
                {
                  type: 'template',
                  templateUrl: basePath + 'actions/workflow/load-spec.html',
                  condition: actionType === 'update'
                },
                {
                  key: 'spec',
                  type: 'textarea',
                  condition: actionType === 'create',
                  readonly: actionType === 'update'
                }
              ]
            },
            {
              type: 'template',
              templateUrl: basePath + 'actions/workflow/policy.help.html'
            }
          ]
        }
      ]; // form

      model = {
        id: '',
        name: '',
        spec: ''
      };

      var config = {
        title: title,
        submitText: submitText,
        schema: schema,
        form: form,
        model: model
      };

      scope.model = model;

      return config;
    }

    return workflow;
  }
})();

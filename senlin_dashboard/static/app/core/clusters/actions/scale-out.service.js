/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
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
   * @ngDoc factory
   * @name horizon.cluster.clusters.actions.scale-in.service
   * @Description
   * restart container.
   */
  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.scale-out.service', scaleService);

  scaleService.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.clusters.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service'
  ];

  function scaleService(
    senlin, resourceType, actionResult, gettext, $qExtensions, modal, toast
  ) {
    // schema
    var schema = {
      type: "object",
      properties: {
        count: {
          title: gettext("Node Count"),
          type: "number",
          minimum: 1
        }
      }
    };

    // form
    var form = [
      {
        type: 'section',
        htmlClass: 'row',
        items: [
          {
            type: 'section',
            htmlClass: 'col-sm-12',
            items: [
              {
                key: "count",
                placeholder: gettext("Specify node count for scale-out.")
              }
            ]
          }
        ]
      }
    ];

    // model
    var model;

    var message = {
      success: gettext('Cluster scale-out %s was successfully accepted.')
    };

    var service = {
      initAction: initAction,
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    // include this function in your service
    // if you plan to emit events to the parent controller
    function initAction() {
    }

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function perform(selected) {
      model = {
        id: selected.id,
        name: selected.name,
        count: null
      };
      // modal config
      var config = {
        title: gettext('Scale-Out'),
        submitText: gettext('Scale-Out'),
        schema: schema,
        form: form,
        model: model
      };
      return modal.open(config).then(submit);

      function submit(context) {
        var id = context.model.id;
        var name = context.model.name;
        delete context.model.id;
        delete context.model.name;
        return senlin.scaleCluster(id, name, 'out', context.model.count).then(function() {
          toast.add('success', interpolate(message.success, [name]));
          var result = actionResult.getActionResult().updated(resourceType, id);
          return result.result;
        });
      }
    }
  }
})();

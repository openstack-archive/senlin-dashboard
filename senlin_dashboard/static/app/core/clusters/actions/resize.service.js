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
   * @name horizon.cluster.clusters.actions.resize.service
   * @Description
   * restart container.
   */
  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.resize.service', resizeService);

  resizeService.$inject = [
    'horizon.app.core.openstack-service-api.senlin',
    'horizon.app.core.clusters.resourceType',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.form.ModalFormService',
    'horizon.framework.widgets.toast.service'
  ];

  function resizeService(
    senlin, resourceType, actionResult, gettext, $qExtensions, modal, toast
  ) {
    // schema
    var schema = {
      type: "object",
      properties: {
        adjustment_type: {
          title: gettext("Type"),
          type: "string"
        },
        number: {
          title: gettext("Number"),
          type: "number"
        },
        min_step: {
          title: gettext("Minimum Step"),
          type: "number",
          minimum: 1
        },
        strict: {
          title: gettext("Specifying whether the resize should be performed on " +
            "a best-effort basis when the new capacity may go beyond size constraints."),
          type: "boolean"
        },
        min_size: {
          title: gettext("Minimum Size"),
          type: "number",
          minimum: 1
        },
        max_size: {
          title: gettext("Maximum Size"),
          type: "number",
          minimum: -1
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
                key: "adjustment_type",
                type: "select",
                titleMap: [
                  {value: '', name: gettext('Select type for resize.')},
                  {value: 'EXACT_CAPACITY', name: gettext('Capacity')},
                  {value: 'CHANGE_IN_CAPACITY', name: gettext('Adjustment')},
                  {value: 'CHANGE_IN_PERCENTAGE', name: gettext('Percentage')}
                ]
              },
              {
                key: "number",
                placeholder: gettext("Specify the number according to the type " +
                  "you selected as follows.")
              },
              {
                type: "template",
                template: "<p>" +
                  gettext("Capacity: The desired number of nodes of the cluster.") +
                  "<br>" +
                  gettext("Adjustment: A positive integer meaning the number of nodes to add, " +
                    "or a negative integer indicating the number of nodes to remove. " +
                    "And this can not be zero.") +
                  "<br>" +
                  gettext("Percentage: A value that is interpreted as the percentage of size " +
                    "adjustment. This value can be positive or negative. " +
                    "And this can not be zero.") +
                  "</p>"
              },
              {
                key: "min_step",
                placeholder: gettext("An integer specifying the number of nodes for adjustment " +
                  "when \"Percentage\" is specified for \"Type\".")
              },
              {
                key: "strict"
              },
              {
                key: "min_size",
                placeholder: gettext("New lower bound of cluster size.")
              },
              {
                key: "max_size",
                placeholder: gettext("New upper bound of cluster size. " +
                  "A value of -1 indicates no upper limit on cluster size.")
              }
            ]
          }
        ]
      }
    ];

    // model
    var model;

    var message = {
      success: gettext('Cluster resize %s was successfully accepted.')
    };

    var service = {
      allowed: allowed,
      perform: perform
    };

    return service;

    //////////////

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function perform(selected) {
      model = {
        id: selected.id,
        name: selected.name,
        adjustment_type: "",
        number: null,
        min_step: null,
        strict: false,
        min_size: null,
        max_size: null
      };
      // modal config
      var config = {
        title: gettext('Resize'),
        submitText: gettext('Resize'),
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
        if (context.model.adjustment_type === "") {
          context.model.adjustment_type = null;
        }
        /*
          model should be like below:
          {
            "adjustment_type": "EXACT_CAPACITY",
            "number": 3,
            "min_step": null,
            "strict": false,
            "min_size": null,
            "max_size": null
          }
         */
        return senlin.resizeCluster(id, name, context.model, false).then(function() {
          toast.add('success', interpolate(message.success, [name]));
          var result = actionResult.getActionResult().updated(resourceType, id);
          return result.result;
        });

        /* NOTE(shu-mutou): form verification is needed for usability.
        function verifyParams(model) {
          if (model.adjustment_type === "" && model.min_size === null && model.max_size === null) {
            toast.add('error',
              gettext("At least one parameter of 'Type' with 'Number', " +
                "'Minumum Size' or 'Maximum Size' should be specified."));
          }
          if (model.adjustment_type === "EXACT_CAPACITY") {
            if (model.number < 0) {
              toast.add('error',
                gettext('Number must be larger than or equal to zero with type \"Capacity\".'));
            }
          }
          else if (model.adjustment_type === "CHANGE_IN_CAPACITY") {
            if (model.number === 0) {
              toast.add('error',
                gettext('Number can not be zero with type \"Adjustment\".'));
            }
          }
          else if (model.adjustment_type === "CHANGE_IN_PERCENTAGE") {
            if (model.number === 0 || model.number === 0.0) {
              toast.add('error',
                gettext('Number can not be zero with type \"Percentage\".'));
            }
          }
          if (model.min_step !== null && model.adjustment_type !== "CHANGE_IN_PERCENTAGE") {
            toast.add('error',
              gettext('Min Step is only used with type \"Percentage\".'));
          }
          if (model.min_size !== null) {
            if (model.min_size < 0) {
              toast.add('error',
                gettext('Min Size can not be less than zero.'));
            }
            if (model.max_size !== null && model.max_size >= 0 && model.min_size > model.max_size) {
              toast.add('error',
                gettext("Min Size can not be larger than max size."));
            }
            if (model.adjustment_type === "CHANGE_IN_CAPACITY" && model.min_size > model.number) {
              toast.add('error',
                gettext("Min Size can not be larger than the specified Number with type " +
                  "\"Capacity\"."));
            }
          }
          if (model.max_size !== null) {
            if (model.adjustment_type === "CHANGE_IN_CAPACITY" &&
              model.max_size > 0 && model.max_size < model.number) {
              toast.add('error',
                gettext("Max Size can not be less than the specified Number with type " +
                  "\"Capacity\"."));
            }
          }
        }
        */
      }
    }
  }
})();

/*
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  "use strict";

  angular
    .module('horizon.cluster.profiles')
    .controller('horizon.cluster.profiles.profileOverviewController', controller);

  controller.$inject = [
    'horizon.app.core.profiles.resourceType',
    'horizon.framework.conf.resource-type-registry.service',
    '$scope'
  ];

  function controller(
    profileResourceType,
    registry,
    $scope
  ) {
    var ctrl = this;
    $scope.context.loadPromise.then(onGetProfile);

    function onGetProfile(profile) {
      ctrl.profile = profile.data;
    }
  }

})();

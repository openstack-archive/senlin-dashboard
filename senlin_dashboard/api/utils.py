# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import itertools
import yaml

from django.utils.translation import ugettext_lazy as _


def update_pagination(entities, request_size, page_size, marker,
                      reversed_order):
    has_prev_data = False
    has_more_data = False

    entities = list(itertools.islice(entities, request_size))
    # first and middle page condition
    if len(entities) > page_size:
        entities.pop(-1)
        has_more_data = True
        # middle page condition
        if marker is not None:
            has_prev_data = True
    # first page condition when reached via prev back
    elif reversed_order and marker is not None:
        has_more_data = True
    # last page condition
    elif marker is not None:
        has_prev_data = True

    # restore the original ordering here
    if reversed_order:
        entities.reverse()

    return entities, has_more_data, has_prev_data


def convert_to_yaml(data, default_flow_style=False):
    if not data:
        return ''
    try:
        return yaml.safe_dump(data, default_flow_style=default_flow_style)
    except Exception:
        return ''


def load_yaml(data):
    if not data:
        loaded_data = {}
    else:
        try:
            loaded_data = yaml.safe_load(data)
        except Exception as ex:
            raise Exception(_('The specified input is not a valid '
                              'YAML format: %s') % ex)
    return loaded_data

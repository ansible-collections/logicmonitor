#!/usr/bin/python

# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: lm_info

short_description: Gather information about LogicMonitor objects (e.g. collectors, collector groups, devices,
                   device groups, etc.).

version_added: "1.0.0"

author:
    - Carlos Alvarenga (@cealvar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module collects information about devices, collectors, devices and device groups associated with your
      LogicMonitor account.

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    target:
        description:
            - The type of LogicMonitor object you wish to query.
        required: true
        choices: ['collector', 'collector_group', 'device', 'device_group', 'alert_rule', 'escalation_chain']
        type: str
    id:
        description:
            - ID of the collector, device, device group, escalation chain, etc to target.
        type: int
    name:
        description:
            - Name of the collector group, alert rule, escalation chain, etc to target.
        type: str
    description:
        description:
            - Description of the collector to target.
        type: str
    display_name:
        description:
            - Display name of the device to target.
        type: str
    hostname:
        description:
            - Name (hostname) of the device to target.
        type: str
    full_path:
        description:
            - Full path of the device group to target.
            - Root group full_path should be denoted by empty string "" or "/".
        type: str
    size:
        description:
            - The number of resources/results to display (max is 1000).
        type: int
        default: 250
'''

EXAMPLES = r'''
# Get all collectors
- name: Get collectors
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get collector
- name: Get collector
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get all collector groups
- name: Get collector groups
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector_group
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get collector group
- name: Get collector group
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector_group
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "collector group"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get all devices
- name: Get devices
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get device
- name: Get device
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: "{{ output }}"

# Get all device groups
- name: Get device groups
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device_group
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: "{{ output }}"

# Get device group
- name: Get device group
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device_group
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get alert rules
- name: Get alert rules
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: alert_rule
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get alert rule
- name: Get alert rule
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: alert_rule
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'
# Get escalation chains
- name: Get escalation chains
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: escalation_chain
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

# Get escalation chain
- name: escalation chain
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: escalation_chain
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

'''

RETURN = r'''
# These are examples of possible return values.
data:
    description: The dictionary containing information about all collectors associated with your account
    type: dict
    returned: always
    sample: {
        'isMin': false,
        'items': [
            {}
        ],
        'searchId': null,
        'total': 1
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

COLLECTOR = "collector"
COLLECTOR_GROUP = "collector_group"
DEVICE = "device"
DEVICE_GROUP = "device_group"
DATA = "data"
SIZE = 500
ALERT_RULE = "alert_rule"
ESCALATION_CHAIN = "escalation_chain"


def retrieve_collector_info(lm):
    lm.module.debug("Running retrieve_collector_details...")
    id = lm.module.params[lm.ModuleFields.ID]
    description = lm.module.params[lm.ModuleFields.DESCRIPTION]

    if lm.valid_id(id) or description is not None:
        return lm.collector_utils.get_collector_info(id, description)
    return lm.collector_utils.get_collectors()


def retrieve_collector_group_info(lm):
    lm.module.debug("Running retrieve_collector_group_info...")
    id = lm.module.params[lm.ModuleFields.ID]
    name = lm.module.params[lm.ModuleFields.NAME]

    if lm.valid_id(id) or name is not None:
        return lm.collector_group_utils.get_collector_group_info(id, name)
    return lm.collector_group_utils.get_collector_groups()


def retrieve_device_info(lm):
    lm.module.debug("Running retrieve_device_details...")
    id = lm.module.params[lm.ModuleFields.ID]
    display_name = lm.module.params[lm.ModuleFields.DISPLAY_NAME]
    hostname = lm.module.params[lm.ModuleFields.HOSTNAME]

    if lm.valid_id(id) or display_name or hostname:
        return lm.device_utils.get_device_info(id, display_name, hostname)
    return lm.device_utils.get_devices()


def retrieve_device_group_info(lm):
    lm.module.debug("Running retrieve_device_group_info...")
    id = lm.module.params[lm.ModuleFields.ID]
    full_path = lm.module.params[lm.ModuleFields.FULL_PATH]

    if lm.valid_id(id) or full_path is not None:
        return lm.device_group_utils.get_device_group_info(id, full_path)
    return lm.device_group_utils.get_device_groups()


def retrieve_alert_rule_info(lm):
    lm.module.debug("Running retrieve_alert_rule_info...")
    id = lm.module.params[lm.ModuleFields.ID]
    name = lm.module.params[lm.ModuleFields.NAME]

    if lm.valid_id(id) or name is not None:
        return lm.alert_rule_utils.get_alert_rule_info(id, name)
    return lm.alert_rule_utils.get_alert_rules()


def retrieve_escalation_chain_info(lm):
    lm.module.debug("Running retrieve_escalation_chain_info...")
    id = lm.module.params[lm.ModuleFields.ID]
    name = lm.module.params[lm.ModuleFields.NAME]

    if lm.valid_id(id) or name is not None:
        return lm.escalation_chain_utils.get_escalation_chain_info(id, name)
    return lm.escalation_chain_utils.get_escalation_chains()


def run():
    """ Run module to obtain information requested by the user """

    targets = [
        COLLECTOR,
        COLLECTOR_GROUP,
        DEVICE,
        DEVICE_GROUP,
        ALERT_RULE,
        ESCALATION_CHAIN
    ]

    module = AnsibleModule(
        argument_spec=dict(
            target=dict(required=True, choices=targets),
            company=dict(required=True),
            domain=dict(required=False, default="logicmonitor.com"),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            name=dict(required=False),
            description=dict(required=False),
            display_name=dict(required=False),
            hostname=dict(required=False),
            full_path=dict(required=False, default=None),
            size=dict(required=False, default=250, type="int")
        ),
        supports_check_mode=True
    )

    lm = LogicMonitorBaseModule(module)
    lm.size = lm.module.params[lm.ModuleFields.SIZE]

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    result = dict(
        changed=False,
        data={},
    )

    # if the user is working with this module in 'only check mode'
    # we do not want to make any changes to the environment,
    # just return current state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    target = lm.module.params[lm.ModuleFields.TARGET]
    if target == COLLECTOR:
        result[DATA] = retrieve_collector_info(lm)
    elif target == COLLECTOR_GROUP:
        result[DATA] = retrieve_collector_group_info(lm)
    elif target == DEVICE:
        result[DATA] = retrieve_device_info(lm)
    elif target == DEVICE_GROUP:
        result[DATA] = retrieve_device_group_info(lm)
    elif target == ALERT_RULE:
        result[DATA] = retrieve_alert_rule_info(lm)
    elif target == ESCALATION_CHAIN:
        result[DATA] = retrieve_escalation_chain_info(lm)
    else:
        lm.fail(msg="Unexpected target \"" + target + "\" was specified.")

    # in the event of a successful module execution, you will want to exit, passing the key/value results
    lm.output_info(result)


def main():
    run()


if __name__ == '__main__':
    main()

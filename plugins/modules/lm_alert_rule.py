#!/usr/bin/python

# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: lm_alert_rule

short_description: LogicMonitor Alert Rule Ansible module for managing alert rules.

version_added: "1.2.0"

author:
    - Gunjan Kumar (@gunjan)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages alert rules within your LogicMonitor account (i.e. add, update, remove).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the alert rule.
            - Add = Add a alert rule to your LogicMonitor account.
            - Update = priority, level, escalation chain etc for a alert rule in your LogicMonitor account.
            - Remove = Remove a alert rule from your LogicMonitor account.
        required: true
        type: str
        choices: ["add", "update", "remove"]
    id:
        description:
            - ID of the alert rule to target.
            - Required for update, remove if name isn't provided.
        type: int
    name:
        description:
            - The name of the alert rule to target.
            - Required for action=add.
            - Required for update, remove if id isn't provided.
        type: str
    priority:
        description:
            - A numeric value determining the priority of alert rule.
            - Number '1' represents the highest priority.
            - Required for action=add.
        type: int
    level:
        description:
            - alert severity level to which the alert rule would apply.
            - Defaults to All when creating rule.
            - Optional for managing alert rule (action=add or action=update)
        type: str
        choices: [All, Warn, Error, Critical]
    datasource:
        description:
            - The datasource for which the alert rule would be applicable.
            - Defaults to all datasource when creating rule.
            - Optional for managing alert rule (action=add or action=update).
        type: str
    datapoint:
        description:
            - The datapoint for which the alert rule would be applicable.
            - Defaults to all datapoint when creating rule.
            - Optional for managing alert rule (action=add or action=update).
        type: str
    instance:
        description:
            - The instance for which the alert rule would be applicable.
            - Defaults to all instance when creating rule.
            - Optional for managing alert rule (action=add or action=update).
        type: str
    groups:
        description:
            - A comma-separated list of device groups for which the rule would be applicable.
            - Defaults to all groups when creating rule.
            - Must be enclosed within [] brackets.
            - Optional for managing alert rule (action=add or action=update).
        type: list
        elements: str
    devices:
        description:
            - A comma-separated list of devices for which the rule would be applicable.
            - Defaults to all devices when creating rule.
            - Must be enclosed within [] brackets.
            - Optional for managing alert rules (action=add or action=update).
        type: list
        elements: str
    suppress_clear:
        description:
            - A boolean flag to enable/disable notification of alert clear.
            - Defaults to False when creating a rule.
            - Optional for managing rules (action=add or action=update).
        type: bool
        choices: [True, False]
    suppress_ACK_STD:
        description:
            - A boolean flag to enable/disable notification of alert SDT and Acknowledge.
            - Defaults to False when creating a rule.
            - Optional for managing rule (action=add or action=update).
        type: bool
        choices: [True, False]
    escalation_chain_id:
        description:
            - ID of escalation chain to which the alert would be sent.
            - Required for action=add.
            - Optional for managing rules action=update.
        type: int
    escalation_interval:
        description:
            - the amount of time(min) that should elapse before an alert will be escalated to the next stage.
            - Required for action=add.
            - Optional for managing rules action=update.
        type: int
    resource_properties_filter:
        description:
            - A JSON object of properties that a resource or website must possess in order for this alert rule to match.
            - A maximum of five property filters can be specified.
            - Multiple property filters are joined by an AND logical operator.
            - Must be enclosed within {} braces.
            - Optional for managing rules (action=add or action=update).
        type: dict
    force_manage:
        description:
            - A boolean flag to enable/disable the feature to ...
              (1) update a alert rule when the initial action=add because the rule exists or
              (2) add a alert rule when the initial action=update because the rule doesn't exist.
            - Optional for managing alert rule (action=add or action=update).
        type: bool
        default: True
        choices: [True, False]
'''

EXAMPLES = r'''
# Example of adding a alert rule
- name: Add Alert Rule
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Alert Rule
      lm_alert_rule:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: AlertRule-12
        priority: 55
        level: All
        escalation_chain_id: 2
        escalation_interval: 23

# Example of updating a alert rule
- name: Update Alert Rule
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Alert Rule
      lm_alert_rule:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
        priority: 55
        level: All
        datasource: Ping
        datapoint: Ping
        instance: Ping
        groups: ["Customer", "Devices by Type"]
        devices: ["192.168.147.131", "127.0.0.1_collector_2"]
        suppress_clear: true
        suppress_ACK_STD: true
        escalation_chain_id: 2
        escalation_interval: 30
        resource_properties_filter : {"key1": "value1","key2": "value2"}

# Example of removing a alert rule
- name: Remove Alert Rule
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Alert Rule
      lm_alert_rule:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "alert rule name"
'''

RETURN = r'''
---
success:
    description: flag indicating that execution was successful
    returned: success
    type: bool
    sample: True
changed:
    description: a boolean indicating that changes were made to the target
    returned: changed
    type: bool
    sample: True
failed:
    description: a boolean indicating that execution failed
    returned: failed
    type: bool
    sample: False
data:
    description: contain alert rule group details
    returned: success
    type: dict
    sample: { "id": 4, "name": "rule_1" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Alert Rule updated successfully"
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule


LEVEL_ALL = "All"
LEVELS = [
    LEVEL_ALL,
    "Warn",
    "Critical",
    "Error"
]


class AlertRule(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize  the LogicMonitor Alert Rule object """

        self.changed = False
        self.action_performed = "None"
        self.result = None
        self.additional_info = ""
        actions = [
            self.ADD,
            self.UPDATE,
            self.REMOVE
        ]

        module_args = dict(
            action=dict(required=True, choices=actions),
            company=dict(required=True),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            name=dict(required=False, type="str"),
            priority=dict(required=False, type="int"),
            level=dict(required=False, type="str", choices=LEVELS),
            groups=dict(required=False, type="list", elements="str"),
            devices=dict(required=False, type="list", elements="str"),
            datasource=dict(required=False, type="str"),
            datapoint=dict(required=False, type="str"),
            instance=dict(required=False, type="str"),
            suppress_clear=dict(required=False, type="bool", choices=[True, False]),
            suppress_ACK_STD=dict(required=False, type="bool", choices=[True, False]),
            escalation_interval=dict(required=False, type="int"),
            escalation_chain_id=dict(required=False, type="int"),
            resource_properties_filter=dict(required=False, type="dict"),
            force_manage=dict(required=False, type="bool", default=True, choices=[True, False])

        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating Alert Rule object")

        self.id = self.params[self.ModuleFields.ID]
        self.name = self.params[self.ModuleFields.NAME]
        self.priority = self.params[self.ModuleFields.PRIORITY]
        self.level = self.params[self.ModuleFields.LEVEL]
        self.groups = self.params[self.ModuleFields.GROUPS]
        self.devices = self.params[self.ModuleFields.DEVICES]
        self.datasource = self.params[self.ModuleFields.DATASOURCE]
        self.datapoint = self.params[self.ModuleFields.DATAPOINT]
        self.instance = self.params[self.ModuleFields.INSTANCE]
        self.suppress_clear = self.params[self.ModuleFields.SUPPRESS_CLEAR]
        self.suppress_ACK_STD = self.params[self.ModuleFields.SUPPRESS_ACK_AND_SDT]
        self.escalation_interval = self.params[self.ModuleFields.ESCALATION_INTERVAL]
        self.escalation_chain_id = self.params[self.ModuleFields.ESCALATION_CHAIN_ID]
        self.resource_properties_filter = self.params[self.ModuleFields.RESOURCE_PROPERTIES]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        # info contains alert rule JSON object (if it exists), None (if it doesn't exist), or an error message from
        # the API (if retrieval failed)
        self.info = self.alert_rule_utils.get_alert_rule_info(self.id, self.name, False)

    def run(self):
        """ Run module to perform action requested by the user """
        self.module.debug("Running module...")
        action = self.module.params[self.ModuleFields.ACTION]
        if action == self.ADD:
            self.add()
        elif action == self.UPDATE:
            self.update()
        elif action == self.REMOVE:
            self.remove()
        else:
            errmsg = ("Unexpected action \"" + str(self.module.params[self.ModuleFields.ACTION]) + "\" was specified.")
            self.fail(errmsg)

        self.exit_with_info()

    def add(self):
        """ Add Alert Rule in your LogicMonitor account """
        self.module.debug("Running AlertRule.add...")

        if self.success_response(self.info):
            # rule exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add alert rule - Alert rule already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # rule doesn't exist
                data = self.build_alert_rule_data()
                self.module.debug("Data: " + str(data))
                response = self.alert_rule_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Alert Rule added successfully"
                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to alert rule existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor alert rule used for monitoring """
        self.module.debug("Running AlertRule.update...")

        if self.success_response(self.info):
            # rule exists
            self.id = self.info[self.ID]
            data = self.build_alert_rule_data()
            self.module.debug("Data: " + str(data))
            response = self.alert_rule_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Alert Rule updated successfully"

            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # rule doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def remove(self):
        """ Remove this alert rule from your LogicMonitor account """
        self.module.debug("Running AlertRule.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        self.alert_rule_utils.send_delete_request(self.id)
        self.action_performed = "remove"
        self.additional_info = "Alert Rule removed successfully"
        self.result = self.get_basic_info()
        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def validate_add_fields(self):
        self.module.debug("Running AlertRule.validate_add_fields...")
        if not self.name:
            self.fail("Invalid arguments - Adding a alert rule requires a unique name.")
        if not self.priority:
            self.fail("Invalid arguments - Adding a alert rule requires priority.")
        if not self.escalation_interval:
            self.fail("Invalid arguments - Adding a alert rule requires escalation interval.")
        if not self.escalation_chain_id:
            self.fail("Invalid arguments - Adding a alert rule requires escalation chain id.")

    def validate_update_fields(self):
        self.module.debug("Running AlertRule.validate_update_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Updating a alert rule requires an existing alert rule id or name.")

    def validate_remove_fields(self):
        self.module.debug("Running AlertRule.validate_remove_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Removing a alert rule requires an existing alert rule id or name.")

    def build_alert_rule_data(self):
        self.module.debug("Running AlertRule.build_alert_rule_data...")
        data = {}
        if self.name is not None:
            data[self.ALERTRULEFields.NAME] = self.name
        if self.priority is not None:
            data[self.ALERTRULEFields.PRIORITY] = self.priority
        if self.level is not None:
            data[self.ALERTRULEFields.LEVEL] = self.level
        if self.datapoint is not None:
            data[self.ALERTRULEFields.DATAPOINT] = self.datapoint
        if self.datasource is not None:
            data[self.ALERTRULEFields.DATASOURCE] = self.datasource
        if self.instance is not None:
            data[self.ALERTRULEFields.INSTANCE] = self.instance
        if self.groups is not None:
            data[self.ALERTRULEFields.GROUPS] = self.groups
        if self.devices is not None:
            data[self.ALERTRULEFields.DEVICES] = self.devices
        if self.suppress_clear is not None:
            data[self.ALERTRULEFields.SUPPRESS_CLEAR] = self.suppress_clear
        if self.suppress_ACK_STD is not None:
            data[self.ALERTRULEFields.SUPPRESS_ALERT_ACK_SDT] = self.suppress_ACK_STD
        if self.escalation_chain_id is not None:
            data[self.ALERTRULEFields.ESCALATION_CHAIN_ID] = self.escalation_chain_id
        if self.escalation_interval is not None:
            data[self.ALERTRULEFields.ESCALATION_INTERVAL] = self.escalation_interval
        if self.resource_properties_filter is not None:
            data[self.ALERTRULEFields.RESOURCE_PROPERTIES] = self.build_properties(self.resource_properties_filter)
        # self.fail(msg=data)
        return data

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " alert rule"
        if not self.info:
            # alert rule doesn't exist
            self.fail(err_msg_template + " - Alert rule doesn't exist")
        else:
            # err msg received from LM not related to alert rule existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: self.info.get(self.ModuleFields.NAME)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: response.get(self.ModuleFields.NAME)}


def main():
    module = AlertRule()
    module.run()


if __name__ == "__main__":
    main()

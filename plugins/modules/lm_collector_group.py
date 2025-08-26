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
module: lm_collector_group

short_description: LogicMonitor Collector Group Ansible module for managing collector groups.

version_added: "1.1.0"

author:
    - Carlos Alvarenga (@cealvar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages collector groups within your LogicMonitor account (i.e. add, update, remove).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the collector group.
            - Add = Add a collector group to your LogicMonitor account.
            - Update = Update properties, description, etc for a collector group in your LogicMonitor account.
            - Remove = Remove a collector group from your LogicMonitor account.
        required: true
        type: str
        choices: ["add", "update", "remove"]
    id:
        description:
            - ID of the collector group to target.
            - Required for update, remove if name isn't provided.
        type: int
    name:
        description:
            - The name of the collector group to target.
            - Default/Ungrouped group name should be denoted by empty string "" or "@default".
            - Required for action=add.
            - Required for update, remove if id isn't provided.
        type: str
    description:
        description:
            - The long text description of the collector group to add.
            - Optional for managing collector groups (action=add or action=update).
        type: str
    properties:
        description:
            - A JSON object of properties to configure for the LogicMonitor collector group.
            - This parameter will add or update existing properties in your LogicMonitor account.
            - Optional for managing collector groups (action=add or action=update).
        type: dict
    auto_balance:
        description:
            - A boolean flag to denote whether or not the collector group should be an Auto-Balanced Collector Group
              (ABCG).
            - Optional for managing collector groups (action=add or action=update).
        type: bool
        choices: [True, False]
    instance_threshold:
        description:
            - The instance count threshold for a Collector in an Auto-Balanced Collector Group (ABCG) is auto-calculated
              using the ABCG's assigned threshold value and the RAM on the Collector machine.
            - By default, this threshold is set to 10,000 instances, which represents the instance count threshold for a
              medium-sized Collector that uses 2 GB of RAM.
            - Only values greater than or equal to 0 will be used.
            - The number of instances that a Collector can handle is calculated with the following formula ...
              * Number of instances = (Target_Collector_mem/Medium_mem)^1/2 * Medium_Threshold.
            - Approximate Instance Thresholds (based on medium-sized Collector threshold limit) ...
              * Small  = 4950 | 7070  | 10600
              * Medium = 7000 | 10000 | 15000
              * Large  = 9900 | 14140 | 21210
        type: int
    force_manage:
        description:
            - A boolean flag to enable/disable the feature to ...
              (1) update a collector group when the initial action=add because the group exists or
              (2) add a collector group when the initial action=update because the group doesn't exist.
            - Optional for managing collector groups (action=add or action=update).
        type: bool
        default: True
        choices: [True, False]
    optype:
        description:
            - A string describing the operation on properties when updating collector group...
              (1) replace - a property would be updated if it exists already else a new property will be created
              (2) refresh - a property would be updated if it exists already else a new property will be created,
                  any existing property not provided during update will be removed
              (3) add - a property would be ignored if it exists already else a new property will be created
            - Optional for action=update.
        type: str
        default: replace
        choices: [add, replace, refresh]
'''

EXAMPLES = r'''
# Example of adding a collector group
- name: Add Collector Group
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Collector Group
      lm_collector_group:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "Collector Group"
        properties: {
            type: dev
        }

# Example of updating a collector group
- name: Update Collector Group
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Collector Group
      lm_collector_group:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 123
        name: "Collector Group New"
        description: "test"
        properties: {
            type2: dev2
        }
        optype: add

# Example of removing a collector group
- name: Remove Collector Group
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Collector Group
      lm_collector_group:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "collector group"
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
    description: contain collector group details
    returned: success
    type: dict
    sample: { "id": 4, "name": "collectors_1" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Collector Group updated successfully"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

CUSTOM_PROPERTIES = "customProperties"
AUTO_BALANCE = "autoBalance"
AUTO_BALANCE_INSTANCE_COUNT_THRESHOLD = "autoBalanceInstanceCountThreshold"


class CollectorGroup(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize the the LogicMonitor Collector Group object """

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
            domain=dict(required=False, default="logicmonitor.com"),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            name=dict(required=False),
            description=dict(required=False),
            properties=dict(required=False, type="dict"),
            auto_balance=dict(required=False, type="bool", choices=[True, False]),
            instance_threshold=dict(required=False, type="int"),
            force_manage=dict(required=False, type="bool", default=True, choices=[True, False]),
            optype=dict(required=False, type="str", default=LogicMonitorBaseModule.ModuleFields.OPTYPE_REPLACE,
                        choices=[LogicMonitorBaseModule.ModuleFields.OPTYPE_REFRESH,
                                 LogicMonitorBaseModule.ModuleFields.OPTYPE_REPLACE,
                                 LogicMonitorBaseModule.ModuleFields.OPTYPE_ADD])
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating Collector Group object")

        self.id = self.params[self.ModuleFields.ID]
        self.name = self.params[self.ModuleFields.NAME]
        self.description = self.params[self.ModuleFields.DESCRIPTION]
        self.properties = self.params[self.ModuleFields.PROPERTIES]
        self.auto_balance = self.params[self.ModuleFields.AUTO_BALANCE]
        self.instance_threshold = self.params[self.ModuleFields.INSTANCE_THRESHOLD]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        self.optype = self.params[self.ModuleFields.OPTYPE]
        # info contains collector group JSON object (if it exists), None (if it doesn't exist), or an error message from
        # the API (if retrieval failed)
        self.info = self.collector_group_utils.get_collector_group_info(self.id, self.name, False)

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
        """ Add collector group for monitoring in your LogicMonitor account """
        self.module.debug("Running CollectorGroup.add...")

        if self.success_response(self.info):
            # group exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add collector group - Collector group already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # group doesn't exist
                data = self.build_collector_group_data()
                self.module.debug("Data: " + str(data))
                response = self.collector_group_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Collector Group added successfully"

                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to collector group existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor collector group used for monitoring """
        self.module.debug("Running CollectorGroup.update...")

        if self.success_response(self.info):
            # group exists
            self.id = self.info[self.ID]
            data = self.build_collector_group_data()
            self.module.debug("Data: " + str(data))
            response = self.collector_group_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Collector Group updated successfully"

            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # group doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def remove(self):
        """ Remove this collector group from your LogicMonitor account """
        self.module.debug("Running CollectorGroup.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        self.collector_group_utils.send_delete_request(self.id)
        self.action_performed = "remove"
        self.additional_info = "Collector Group removed successfully"
        self.result = self.get_basic_info()
        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def validate_add_fields(self):
        self.module.debug("Running CollectorGroup.validate_add_fields...")
        if not self.name:
            self.fail("Invalid arguments - Adding a collector group requires a unique name.")

    def validate_update_fields(self):
        self.module.debug("Running CollectorGroup.validate_update_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Updating a collector group requires an existing collector group id or name.")

    def validate_remove_fields(self):
        self.module.debug("Running CollectorGroup.validate_remove_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Removing a collector group requires an existing collector group id or name.")

    def build_collector_group_data(self):
        self.module.debug("Running CollectorGroup.build_collector_group_data...")
        data = {}
        if self.instance_threshold is not None:
            if self.instance_threshold < 0:
                self.fail("Invalid argument - instance_threshold cannot be less than 0.")
            else:
                data[AUTO_BALANCE_INSTANCE_COUNT_THRESHOLD] = self.instance_threshold
        if self.name:
            data[self.NAME] = self.name.strip()
        if self.description is not None:
            data[self.DESCRIPTION] = self.description
        if self.properties is not None:
            data[CUSTOM_PROPERTIES] = self.build_properties(self.properties)
        if self.auto_balance is not None:
            data[AUTO_BALANCE] = self.auto_balance
        return data

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " collector group"
        if not self.info:
            # collector group doesn't exist
            self.fail(err_msg_template + " - Collector group doesn't exist")
        else:
            # err msg received from LM not related to collector group existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: self.info.get(self.ModuleFields.NAME)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: response.get(self.ModuleFields.NAME)}


def main():
    module = CollectorGroup()
    module.run()


if __name__ == "__main__":
    main()

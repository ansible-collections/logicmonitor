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
module: lm_device_group

short_description: LogicMonitor Device Group Ansible module for managing device groups.

version_added: "1.0.0"

author:
    - Carlos Alvarenga (@cealvar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages device groups within your LogicMonitor account (i.e. add, update, remove, sdt).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options
    - logicmonitor.integration.lm_sdt_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the device group.
            - Add = Add a device group to your LogicMonitor account.
            - Update = Update properties, description, etc for a device group in your LogicMonitor account.
            - Remove = Remove a device group from your LogicMonitor account.
            - SDT = Schedule downtime for a device group in your LogicMonitor account.
        required: true
        type: str
        choices: ["add", "update", "remove", "sdt"]
    id:
        description:
            - ID of the device group to target.
            - Required for update, remove, sdt if full_path isn't provided.
        type: int
    full_path:
        description:
            - The full path of the device group to target.
            - Root group full_path should be denoted by empty string "" or "/".
            - Required for action=add.
            - Required for update, remove, sdt if id isn't provided.
        type: str
    collector_id:
        description:
            - ID of preferred collector to monitor newly added device group.
            - Optional for managing device groups (action=add or action=update).
        type: int
    collector_description:
        description:
            - Description of preferred collector to monitor newly added device group.
            - Optional for managing device groups (action=add or action=update).
        type: str
    description:
        description:
            - The long text description of the device group to add.
            - Optional for managing device groups (action=add or action=update).
        type: str
    disable_alerting:
        description:
            - A boolean flag to turn alerting on or off for a device groups.
            - Defaults to False when creating a device group.
            - Optional for managing device groups (action=add or action=update).
        type: bool
        choices: [True, False]
    properties:
        description:
            - A JSON object of properties to configure for the LogicMonitor device group.
            - This parameter will add or update existing properties in your LogicMonitor account.
            - Optional for managing device groups (action=add or action=update).
        type: dict
    datasource_id:
        description:
            - The ID of the device group datasource in your LogicMonitor account to SDT.
            - If datasource_id & datasource_name are not supplied for device group SDT, all datasources under the group
              are SDT'd.
            - Optional for action=sdt.
        type: int
    datasource_name:
        description:
            - The name of the device group datasource in your LogicMonitor account to SDT.
            - If datasource_id & datasource_name are not supplied for device group SDT, all datasources under the group
              are SDT'd.
            - Optional for action=sdt.
        type: str
    force_manage:
        description:
            - A boolean flag to enable/disable the feature to ...
              (1) update a device group when the initial action=add because the group exists or
              (2) add a device group when the initial action=update because the group doesn't exist.
            - Optional for managing device groups (action=add or action=update).
        type: bool
        default: True
        choices: [True, False]
    optype:
        description:
            - A string describing the operation on properties when updating device group...
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
# Example of adding a device group
- name: Add Device Group
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Device Group
      lm_device_group:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors/Ansible Group"
        collector_id: 1
        description: "test"
        disable_alerting: true
        properties: {
            snmp.community: commstring,
            type: dev
        }

# Example of updating a device group
- name: Update Device Group
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Device Group
      lm_device_group:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
        collector_id: 1
        description: "test"
        disable_alerting: true
        properties: {
            snmp.community: commstring,
            type: dev
        }
        optype: add

# Example of removing a device group
- name: Remove Device Group
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Device Group
      lm_device_group:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 123

# Example of putting a device group in SDT
- name: SDT Device Group
  hosts: localhost
  tasks:
    - name: Place LogicMonitor device group into Scheduled downtime (default is 30 min.)
      lm_device_group:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
        datasource_id: 123
        datasource_name: "ping"
        duration: 60
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
    description: contain device group details
    returned: success
    type: dict
    sample: { "id": 4, "name": "aws_devices" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Device Group updated successfully"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

PARENT_ID = "parentId"
DISABLE_ALERTING = "disableAlerting"
DEFAULT_COLLECTOR_ID = "defaultCollectorId"
CUSTOM_PROPERTIES = "customProperties"

DEVICE_GROUP_ID = "deviceGroupId"
DEVICE_GROUP_FULL_PATH = "deviceGroupFullPath"
DATASOURCE_ID = "dataSourceId"
DATASOURCE_NAME = "dataSourceName"
FULL_PATH = "fullPath"


class DeviceGroup(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize the the LogicMonitor Device Group object """

        self.changed = False
        self.action_performed = "None"
        self.result = None
        self.additional_info = ""
        actions = [
            self.ADD,
            self.UPDATE,
            self.REMOVE,
            self.SDT
        ]

        module_args = dict(
            action=dict(required=True, choices=actions),
            company=dict(required=True),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            full_path=dict(required=False),
            collector_id=dict(required=False, type="int"),
            collector_description=dict(required=False),
            description=dict(required=False),
            disable_alerting=dict(required=False, type="bool", choices=[True, False]),
            properties=dict(required=False, type="dict"),
            datasource_id=dict(required=False, type="int"),
            datasource_name=dict(required=False),
            start_time=dict(required=False, default=""),
            end_time=dict(required=False, default=""),
            duration=dict(required=False, default=30, type="int"),
            comment=dict(required=False, default=""),
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
        self.module.debug("Instantiating Device Group object")

        self.id = self.params[self.ModuleFields.ID]
        self.full_path = self.params[self.ModuleFields.FULL_PATH]
        if self.full_path is not None:
            self.full_path = self.full_path.strip()
            self.device_group_utils.check_group_path(self.full_path)
        self.collector_id = self.params[self.ModuleFields.COLLECTOR_ID]
        self.collector_desc = self.params[self.ModuleFields.COLLECTOR_DESCRIPTION]
        self.description = self.params[self.ModuleFields.DESCRIPTION]
        self.disable_alerting = self.params[self.ModuleFields.DISABLE_ALERTING]
        self.properties = self.params[self.ModuleFields.PROPERTIES]
        self.datasource_id = self.params[self.ModuleFields.DATASOURCE_ID]
        self.datasource_name = self.params[self.ModuleFields.DATASOURCE_NAME]
        self.start_time = self.process_field(self.params[self.ModuleFields.START_TIME])
        self.end_time = self.process_field(self.params[self.ModuleFields.END_TIME])
        self.duration = self.process_field(self.params[self.ModuleFields.DURATION], 30)
        self.comment = self.params[self.ModuleFields.COMMENT]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        self.optype = self.params[self.ModuleFields.OPTYPE]
        # info contains device group JSON object (if it exists), None (if it doesn't exist), or an error message from
        # the API (if retrieval failed)
        self.info = self.device_group_utils.get_device_group_info(self.id, self.full_path, False)

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
        elif action == self.SDT:
            self.sdt()
        else:
            errmsg = ("Unexpected action \"" + str(self.module.params[self.ModuleFields.ACTION]) + "\" was specified.")
            self.fail(errmsg)

        self.exit_with_info()

    def add(self):
        """ Add device group for monitoring in your LogicMonitor account """
        self.module.debug("Running DeviceGroup.add...")

        if self.success_response(self.info):
            # group exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add device group - Device group already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # group doesn't exist
                data = self.build_device_group_data()
                self.module.debug("Data: " + str(data))
                response = self.device_group_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Device Group added successfully"

                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to device group existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor device group used for monitoring """
        self.module.debug("Running DeviceGroup.update...")

        if self.success_response(self.info):
            # group exists
            self.id = self.info[self.ID]
            data = self.build_device_group_data()
            self.module.debug("Data: " + str(data))
            response = self.device_group_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Device Group updated successfully"

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
        """ Remove this device group from your LogicMonitor account """
        self.module.debug("Running DeviceGroup.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        err_msg = "Failed to delete device group " + str(self.id)
        self.rest_request(self.DELETE, self.DEVICE_GROUPS_BASE_URL + '/' + str(self.id), err_msg=err_msg)

        self.action_performed = "remove"
        self.additional_info = "Device Group removed successfully"
        self.result = self.get_basic_info()

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def sdt(self):
        """ Schedule down time for this device group """
        self.module.debug("Running DeviceGroup.sdt...")

        sdt_interval = self.get_sdt_interval(
            self.start_time, self.end_time, self.duration)

        data = {
            self.SDTFields.TYPE: self.SDTFields.RESOURCE_GROUP_SDT,
            self.SDTFields.SDT_TYPE: self.SDTFields.ONE_TIME,
            self.SDTFields.START_DATE_TIME: sdt_interval[0],
            self.SDTFields.END_DATE_TIME: sdt_interval[1],
            self.SDTFields.COMMENT: self.comment
        }
        self.update_sdt_data(data)

        err_msg = "Failed to SDT device group \ndata: " + str(data)
        response = self.rest_request(self.POST, self.SDT_URL, data, err_msg=err_msg)
        self.action_performed = "sdt"
        self.additional_info = "Device Group SDT successful"
        self.result = self.get_sdt_info_from_response(response)

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit(changed=True)

    def validate_add_fields(self):
        self.module.debug("Running DeviceGroup.validate_add_fields...")
        if not self.full_path or self.full_path == "/":
            self.fail("Invalid arguments - Adding a device group requires a unique full_path.")

    def validate_update_fields(self):
        self.module.debug("Running DeviceGroup.validate_update_fields...")
        if not self.valid_id(self.id) and self.full_path is None:
            self.fail("Invalid arguments - Updating a device group requires an existing device group id or full_path.")

    def is_device_group_exists_err(self, resp):
        self.module.debug("Running DeviceGroup.is_device_group_exists_err...")
        return resp[self.ERROR_CODE] == 1400 and "already exists" in resp[self.ERROR_MESSAGE]

    def build_device_group_data(self):
        self.module.debug("Running DeviceGroup.build_device_group_data...")
        data = {}
        if self.valid_id(self.collector_id) or self.collector_desc is not None:
            data[DEFAULT_COLLECTOR_ID] = self.collector_utils.get_collector_id(self.collector_id, self.collector_desc)
        if self.full_path and self.full_path != "/":
            parent_group, name = self.split_full_path()
            data[self.NAME] = name.strip()
            data[PARENT_ID] = self.retrieve_parent_id(parent_group)
        if self.description is not None:
            data[self.DESCRIPTION] = self.description
        if self.disable_alerting is not None:
            data[DISABLE_ALERTING] = str(self.disable_alerting)
        if self.properties is not None:
            data[CUSTOM_PROPERTIES] = self.build_properties(self.properties)
        return data

    def split_full_path(self):
        self.module.debug("Running DeviceGroup.split_full_path...")
        if self.full_path:
            self.full_path = self.full_path.rstrip("/")
            if not self.full_path.startswith("/"):
                self.full_path = "/" + self.full_path
            return self.full_path.rsplit("/", 1)

    def retrieve_parent_id(self, parent_group):
        self.module.debug("Running DeviceGroup.retrieve_parent_id...")
        return self.device_group_utils.get_new_or_existing_group_id(parent_group)

    def update_sdt_data(self, data):
        """ Add data fields for device group SDTing """
        self.module.debug("Running DeviceGroup.update_sdt_data...")

        if self.valid_id(self.id) or self.full_path is not None:
            if self.success_response(self.info):
                data[DEVICE_GROUP_ID] = self.info[self.ID]
            else:
                self.handle_error_response()
        else:
            self.fail("Invalid arguments - This SDT action requires the device group id (greater than 0) or full_path. "
                      "You may also provide the group device datasource_id and/or datasource_name.")

        if self.valid_id(self.datasource_id):
            data[DATASOURCE_ID] = self.datasource_id
        if self.datasource_name:
            data[DATASOURCE_NAME] = self.datasource_name.strip()

    def validate_remove_fields(self):
        self.module.debug("Running DeviceGroup.validate_remove_fields...")
        if not self.valid_id(self.id) and self.full_path is None:
            self.fail("Invalid arguments - Removing a device group requires an existing device group id or full_path.")

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " device group"
        if not self.info:
            # device group doesn't exist
            self.fail(err_msg_template + " - Device group doesn't exist")
        else:
            # err msg received from LM not related to device group existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.FULL_PATH: self.info.get(FULL_PATH),
                self.ModuleFields.NAME: self.info.get(self.ModuleFields.NAME)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.FULL_PATH: response.get(FULL_PATH),
                self.ModuleFields.NAME: response.get(self.ModuleFields.NAME)}

    def get_sdt_info_from_response(self, response):
        return {self.ModuleFields.START_TIME: response.get(self.SDTFields.START_DATE_TIME_ON_LOCAL),
                self.ModuleFields.END_TIME: response.get(self.SDTFields.END_DATE_TIME_ON_LOCAL),
                self.ModuleFields.DURATION: response.get(self.ModuleFields.DURATION),
                self.ModuleFields.DEVICE_GROUP_ID: response.get(DEVICE_GROUP_ID)}


def main():
    module = DeviceGroup()
    module.run()


if __name__ == "__main__":
    main()

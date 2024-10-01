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
module: lm_device

short_description: LogicMonitor Device Ansible module for managing devices.

version_added: "1.0.0"

author:
    - Carlos Alvarenga (@cealvar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages devices within your LogicMonitor account (i.e. add, update, remove, sdt).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options
    - logicmonitor.integration.lm_sdt_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the device.
            - Add = Add a device to your LogicMonitor account.
            - Update = Update properties, description, etc for a device in your LogicMonitor account.
            - Remove = Remove a device from your LogicMonitor account.
            - SDT = Schedule downtime for a device in your LogicMonitor account.
        required: true
        type: str
        choices: ["add", "update", "remove", "sdt"]
    id:
        description:
            - ID of the device to target.
            - Required for update, remove, sdt if both display_name and hostname aren't provided.
        type: int
    display_name:
        description:
            - The display name of a device (host) in your LogicMonitor account.
            - Required for action=add.
            - Required for update, remove, sdt if both id and hostname aren't provided.
        type: str
    hostname:
        description:
            - The hostname (name) of a device (host) in your LogicMonitor account.
            - Required for action=add.
            - Required for update, remove, sdt if both id and display_name aren't provided.
        type: str
    auto_balance:
        description:
            - A boolean flag to denote whether or not the collector group configured for the device should use
              auto balancing.
            - This value should only be True when the configured collector group is an Auto-Balanced Collector Group
              (ABCG).
            - Optional for managing devices (action=add or action=update).
        type: bool
        choices: [True, False]
    collector_group_id:
        description:
            - ID of the collector group to configure for the device.
            - Required for action=add if an ABCG is being configured (auto_balance=True)
              and collector_group_name isn't provided.
        type: int
    collector_group_name:
        description:
            - Name of the collector group to configure for the device.
            - Default/Ungrouped group name should be denoted by empty string "" or "@default".
            - Required for action=add if an ABCG is being configured (auto_balance=True)
              and collector_group_name isn't provided.
        type: str
    collector_id:
        description:
            - ID of a collector to monitor newly added device.
            - Required for action=add if a non-ABCG is being configured (auto_balance=False)
              and collector_description isn't provided.
            - NOTE - A collector can't be manually configured for an existing device (action=update) when an ABCG is in
                     use and auto balance isn't being disabled.
        type: int
    collector_description:
        description:
            - Description of a collector to monitor newly added device.
            - Required for action=add if a non-ABCG is being configured (auto_balance=False)
              and collector_id isn't provided.
            - NOTE - A collector can't be manually configured for an existing device (action=update) when an ABCG is in
                     use and auto balance isn't being disabled.
        type: str
    groups:
        description:
            - A comma-separated list of device groups that the device should be a member of.
            - The list can contain device group IDs and/or full paths.
            - Must be enclosed within [] brackets.
            - Optional for managing devices (action=add or action=update).
        type: list
        elements: str
    description:
        description:
            - The long text description of the device to add.
            - Optional for managing devices (action=add or action=update).
        type: str
    disable_alerting:
        description:
            - A boolean flag to enable/disable alerting for a device.
            - Defaults to False when creating a device.
            - Optional for managing devices (action=add or action=update).
        type: bool
        choices: [True, False]
    properties:
        description:
            - A JSON object of properties to configure for the LogicMonitor device.
            - This parameter will add or update existing properties in your LogicMonitor account.
            - Must be enclosed within {} braces.
            - Optional for managing devices (action=add or action=update).
        type: dict
    force_manage:
        description:
            - A boolean flag to enable/disable the feature to ...
              (1) update a device when the initial action=add because the device exists or
              (2) add a device when the initial action=update because the device doesn't exist.
            - Optional for managing devices (action=add or action=update).
        type: bool
        default: True
        choices: [True, False]
    optype:
        description:
            - A string describing the operation on properties when updating device...
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
# Example of adding a device
- name: Add Device
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Device
      lm_device:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "Ansible Device"
        hostname: 127.0.0.1
        collector_id: 1
        groups: ["Devices by Type/Misc", 4]
        description: "test"
        disable_alerting: true
        properties: {
            snmp.community: commstring,
            type: dev
        }

# Example of updating a device
- name: Update Device
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Device
      lm_device:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1
        display_name: "New Ansible Device"
        hostname: 127.0.0.1
        collector_description: "localhost 123"
        groups: ["Devices by Type/Misc", 4]
        description: "test"
        disable_alerting: true
        properties: {
            snmp.community: commstring,
            type: dev
        }
        optype: add

# Example of removing a device
- name: Remove Device
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Device
      lm_device:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "Ansible_Device"

# Example of putting a device in SDT
- name: SDT Device
  hosts: localhost
  tasks:
    - name: Place LogicMonitor device into Scheduled downtime (default is 30 min.)
      logicmonitor:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "127.0.0.1_collector_4"
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
    description: contain device or sdt details
    returned: success
    type: dict
    sample: { "id": 13, "hostname": "192.168.147.188", "display_name" : "new_device"}
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Device updated successfully"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

DEVICE_ID = "deviceId"
DEVICE_DISPLAY_NAME = "deviceDisplayName"

DISPLAY_NAME = "displayName"
LINK = "link"
PREFERRED_COLLECTOR_GROUP_ID = "preferredCollectorGroupId"
PREFERRED_COLLECTOR_ID = "preferredCollectorId"
HOST_GROUP_IDS = "hostGroupIds"
DISABLE_ALERTING = "disableAlerting"
CUSTOM_PROPERTIES = "customProperties"
AUTO_BALANCE_COLLECTOR_GROUP_ID = "autoBalancedCollectorGroupId"


class Device(LogicMonitorBaseModule):

    def __init__(self):
        """ Initialize the the LogicMonitor Device object """

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
            display_name=dict(required=False),
            hostname=dict(required=False),
            link=dict(required=False),
            auto_balance=dict(required=False, type="bool", choices=[True, False]),
            collector_group_id=dict(required=False, type="int"),
            collector_group_name=dict(required=False),
            collector_id=dict(required=False, type="int"),
            collector_description=dict(required=False),
            groups=dict(required=False, type="list", elements="str"),
            description=dict(required=False),
            disable_alerting=dict(required=False, type="bool", choices=[True, False]),
            properties=dict(required=False, type="dict"),
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
        self.module.debug("Instantiating Device object")

        self.id = self.params[self.ModuleFields.ID]
        self.display_name = self.params[self.ModuleFields.DISPLAY_NAME]
        self.hostname = self.params[self.ModuleFields.HOSTNAME]
        self.link = self.params[self.ModuleFields.LINK]
        self.auto_balance = self.params[self.ModuleFields.AUTO_BALANCE]
        self.collector_group_id = self.params[self.ModuleFields.COLLECTOR_GROUP_ID]
        self.collector_group_name = self.params[self.ModuleFields.COLLECTOR_GROUP_NAME]
        self.collector_id = self.params[self.ModuleFields.COLLECTOR_ID]
        self.collector_desc = self.params[self.ModuleFields.COLLECTOR_DESCRIPTION]
        self.groups = self.process_groups(self.params[self.ModuleFields.GROUPS])
        self.description = self.params[self.ModuleFields.DESCRIPTION]
        self.disable_alerting = self.params[self.ModuleFields.DISABLE_ALERTING]
        self.properties = self.params[self.ModuleFields.PROPERTIES]
        self.start_time = self.process_field(self.params[self.ModuleFields.START_TIME])
        self.end_time = self.process_field(self.params[self.ModuleFields.END_TIME])
        self.duration = self.process_field(self.params[self.ModuleFields.DURATION], 30)
        self.comment = self.params[self.ModuleFields.COMMENT]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        self.optype = self.params[self.ModuleFields.OPTYPE]
        # info contains device JSON object (if it exists), None (if it doesn't exist), or an error message from the API
        # (if retrieval failed)
        self.info = self.device_utils.get_device_info(self.id, self.display_name, self.hostname, False)

    def process_groups(self, group_list):
        """ Trim leading/trailing spaces from each element of the group list  """
        self.module.debug("Running Device,process_groups...")
        new_group_list = None
        if group_list is not None:
            new_group_list = []
            for group in group_list:
                new_group_list.append(group.strip())
        return new_group_list

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
        """ Add device for monitoring in your LogicMonitor account """
        self.module.debug("Running Device.add...")

        # info contains device JSON object (if it exists), None (if it doesn't exist),
        # or an error message from the API (if retrieval failed)
        if self.success_response(self.info):
            # device exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add - Device already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # device doesn't exist
                data = self.build_device_data()
                self.module.debug("Data: " + str(data))
                response = self.device_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Device added successfully"
                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to device existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor device used for monitoring """
        self.module.debug("Running Device.update...")

        if self.success_response(self.info):
            # device exists
            self.id = self.info[self.ID]
            data = self.build_device_data()
            self.module.debug("Data: " + str(data))
            response = self.device_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Device updated successfully"

            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # device doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def remove(self):
        """ Remove this device from monitoring in your LogicMonitor account """
        self.module.debug("Running Device.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        err_msg = "Failed to delete device " + str(self.id)
        self.rest_request(self.DELETE, self.DEVICES_BASE_URL + '/' + str(self.id), err_msg=err_msg)

        self.action_performed = "remove"
        self.additional_info = "Device removed successfully"
        self.result = self.get_basic_info()
        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def sdt(self):
        """ Schedule down time for this device """
        self.module.debug("Running Device.sdt...")

        sdt_interval = self.get_sdt_interval(self.start_time, self.end_time, self.duration)

        data = {
            self.SDTFields.TYPE: self.SDTFields.RESOURCE_SDT,
            self.SDTFields.SDT_TYPE: self.SDTFields.ONE_TIME,
            self.SDTFields.START_DATE_TIME: sdt_interval[0],
            self.SDTFields.END_DATE_TIME: sdt_interval[1],
            self.SDTFields.COMMENT: self.comment
        }
        self.update_sdt_data(data)

        err_msg = "Failed to SDT device \ndata: " + str(data)
        response = self.rest_request(self.POST, self.SDT_URL, data, err_msg=err_msg)
        self.action_performed = "sdt"
        self.additional_info = "Device SDT successful"
        self.result = self.get_sdt_info_from_response(response)

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def validate_add_fields(self):
        self.module.debug("Running Device.validate_add_fields...")
        err_msg = None
        if not self.hostname or not self.display_name:
            err_msg = "Invalid arguments - Adding a device requires the display_name and hostname"
        elif not self.auto_balance and not self.valid_id(self.collector_id) and self.collector_desc is None:
            err_msg = "Invalid arguments - Adding a device requires the collector_id or collector_description"
        elif self.auto_balance and not self.valid_id(self.collector_group_id) and self.collector_group_name is None:
            err_msg = "Invalid arguments - Enabling auto balancing for a device requires the " \
                      "Auto-Balanced Collector Group ID (collector_group_id) or name (collector_group_name)"
        if err_msg:
            self.fail(err_msg)
        self.verify_groups()

    def verify_groups(self):
        self.module.debug("Running Device.verify_groups...")
        if self.groups:
            for group in self.groups:
                if self.is_int(group) and not self.valid_id(int(group)):
                    self.fail("Invalid group ID: " + str(group))
                else:
                    self.device_group_utils.check_group_path(group)

    def validate_update_fields(self):
        self.module.debug("Running Device.validate_update_fields...")
        err_msg = "Invalid arguments - Updating a device requires one of the following device fields: " \
                  "(1) id (greater than 0), " \
                  "(2) display_name, " \
                  "(3) hostname"
        if not self.valid_id(self.id) and self.hostname is None and self.display_name is None:
            self.fail(err_msg)

    def validate_remove_fields(self):
        self.module.debug("Running Device.validate_remove_fields...")
        err_msg = "Invalid arguments - Removing a device requires one of the following device fields: " \
                  "(1) id (greater than 0), " \
                  "(2) display_name, " \
                  "(3) hostname"
        if not self.valid_id(self.id) and not self.display_name and not self.hostname:
            self.fail(err_msg)

    def build_device_data(self):
        self.module.debug("Running Device.build_device_data...")
        data = {}
        if self.display_name is not None:
            data[DISPLAY_NAME] = self.display_name.strip()
        if self.hostname is not None:
            data[self.NAME] = self.hostname.strip()
        if self.link is not None:
            data[LINK] = self.link.strip()
        data = self.build_collector_data(data)
        if self.groups is not None:
            data[HOST_GROUP_IDS] = self.build_group_ids_list_str()
        if self.description is not None:
            data[self.DESCRIPTION] = self.description
        if self.disable_alerting is not None:
            data[DISABLE_ALERTING] = str(self.disable_alerting)
        if self.properties is not None:
            data[CUSTOM_PROPERTIES] = self.build_properties(self.properties)
        return data

    def build_collector_data(self, data):
        collector_group_provided = self.valid_id(self.collector_group_id) or self.collector_group_name is not None
        if not self.auto_balance:
            if self.auto_balance is False:
                # disable auto balancing
                data[AUTO_BALANCE_COLLECTOR_GROUP_ID] = 0
            elif AUTO_BALANCE_COLLECTOR_GROUP_ID in data and self.valid_id(data[AUTO_BALANCE_COLLECTOR_GROUP_ID]) \
                    and collector_group_provided:
                # configuring new ABCG for existing device that has auto balancing enabled
                data[AUTO_BALANCE_COLLECTOR_GROUP_ID] = \
                    self.collector_group_utils.get_collector_group_id(self.collector_group_id,
                                                                      self.collector_group_name)
            if self.valid_id(self.collector_id) or self.collector_desc is not None:
                # configuring collector for new/existing device
                # this value is irrelevant if auto balancing is enabled for an existing device
                data[PREFERRED_COLLECTOR_ID] = \
                    self.collector_utils.get_collector_id(self.collector_id, self.collector_desc)
        elif collector_group_provided:
            # configuring new ABCG for new, existing device
            data[AUTO_BALANCE_COLLECTOR_GROUP_ID] = \
                self.collector_group_utils.get_collector_group_id(self.collector_group_id, self.collector_group_name)
        elif PREFERRED_COLLECTOR_GROUP_ID in data:
            # enabling auto balancing for existing device -- use same collector group
            data[AUTO_BALANCE_COLLECTOR_GROUP_ID] = data[PREFERRED_COLLECTOR_GROUP_ID]
        return data

    def build_group_ids_list_str(self):
        """
        Return comma-separated list string of group IDs.
        Return empty string if no groups are provided
        """
        self.module.debug("Running Device.build_group_ids_list_str...")
        ids_str = ""
        for group in self.groups:
            group_id = self.get_device_group_id(group)
            ids_str += str(group_id) + ","
        return ids_str.rstrip(",")

    def get_device_group_id(self, val):
        self.module.debug("Running DeviceGroup.get_device_group_id...")
        if val.isdigit():
            return val
        else:
            val = val.strip().rstrip("/")
            if not val.startswith("/"):
                val = "/" + val
            return self.device_group_utils.get_new_or_existing_group_id(val)

    def update_sdt_data(self, data):
        """ Add data fields for device SDTing """
        self.module.debug("Running Device.update_sdt_data...")
        if self.valid_id(self.id) or self.display_name or self.hostname:
            if self.success_response(self.info):
                data[DEVICE_ID] = self.info[self.ID]
            else:
                self.handle_error_response()
        else:
            self.fail("Invalid arguments - "
                      "This SDT action requires the device id (greater than 0), display_name, or hostname.")

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " device"
        if not self.info:
            # device doesn't exist
            self.fail(err_msg_template + " - Device doesn't exist")
        else:
            # err msg received from LM not related to device existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.HOSTNAME: self.info.get(self.NAME),
                self.ModuleFields.DISPLAY_NAME: self.info.get(DISPLAY_NAME)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.HOSTNAME: response.get(self.NAME),
                self.ModuleFields.DISPLAY_NAME: response.get(DISPLAY_NAME)}

    def get_sdt_info_from_response(self, response):
        return {self.ModuleFields.START_TIME: response.get(self.SDTFields.START_DATE_TIME_ON_LOCAL),
                self.ModuleFields.END_TIME: response.get(self.SDTFields.END_DATE_TIME_ON_LOCAL),
                self.ModuleFields.DURATION: response.get(self.ModuleFields.DURATION),
                self.SDTFields.SDT_ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.DEVICE_ID: response.get(DEVICE_ID)}


def main():
    module = Device()
    module.run()


if __name__ == "__main__":
    main()

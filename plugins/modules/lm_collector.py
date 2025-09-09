#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022-2025, LogicMonitor, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: lm_collector

short_description: Manage LogicMonitor collectors

version_added: "1.0.0"

author:
  - Carlos Alvarenga (@cealvar)
  - Madhvi Jain (@madhvi-jain)

description:
  - Add, update, remove LogicMonitor collectors, or place a collector into scheduled downtime (SDT).

options:
  action:
    description:
      - The action to perform on the collector.
      - C(add) to create or install a collector.
      - C(update) to modify an existing collector.
      - C(remove) to delete/uninstall a collector.
      - C(sdt) to schedule downtime for a collector.
    type: str
    required: true
    choices: ['add', 'update', 'remove', 'sdt']

  company:
    description:
      - LogicMonitor account company name (e.g. C(batman) for C(batman.logicmonitor.com)).
    type: str
    required: true

  domain:
    description:
      - LogicMonitor account domain suffix (e.g. C(lmgov.us) for C(batman.lmgov.us)).
    type: str
    default: logicmonitor.com

  access_id:
    description:
      - LogicMonitor API Access ID.
    type: str
    required: true

  access_key:
    description:
      - LogicMonitor API Access Key. If it begins with a special character, prefix with C(!unsafe) in playbooks.
    type: str
    required: true

  id:
    description:
      - Collector ID.
      - Required for C(update), C(remove), C(sdt) if I(description) is not provided.
      - Optional for C(add) (when installing an existing collector).
    type: int

  description:
    description:
      - Collector description.
      - Optional for C(add).
      - Required for C(update), C(remove), C(sdt) if I(id) is not provided.
      - Optional for C(add) when installing an existing collector.
    type: str

  install_path:
    description:
      - Directory where the collector agent is or will be installed.
    type: str
    default: /usr/local/logicmonitor

  install_user:
    description:
      - Username to associate with the installed collector.
    type: str
    default: logicmonitor

  collector_group_id:
    description:
      - ID of the collector group to associate with the collector (C(add)).
    type: int

  collector_group_name:
    description:
      - Name of the collector group to associate with the collector (C(add)).
      - Use empty string C("") or C(@default) for the default (Ungrouped) collector group.
    type: str

  device_group_id:
    description:
      - ID of the device group to associate with the collector (C(add)).
    type: int

  device_group_full_path:
    description:
      - Full path of the device group to associate with the collector (C(add)).
      - Use empty string C("") or C(/) for the root group.
    type: str

  platform:
    description:
      - Target platform string (e.g. C(Linux)).
    type: str

  version:
    description:
      - Collector version to download and install. Defaults to the latest generally available version if omitted.
    type: str

  size:
    description:
      - Collector size profile to install (C(add)).
    type: str
    default: small
    choices: ['nano', 'small', 'medium', 'large']

  escalating_chain_id:
    description:
      - ID of the escalation chain to configure (C(update)).
      - C(0) disables alert routing/notifications.
    type: int

  escalating_chain_name:
    description:
      - Name of the escalation chain to configure (C(update)).
    type: str

  backup_collector_id:
    description:
      - ID of the failover collector to configure (C(update)).
      - C(0) removes any failover collector.
    type: int

  backup_collector_description:
    description:
      - Long description of the failover collector to configure (C(update)).
    type: str

  resend_collector_down_alert_interval:
    description:
      - Interval, in minutes, after which collector down alerts are resent.
      - C(0) sends the collector down alert only once.
    type: int

  properties:
    description:
      - Dictionary of properties to set on the collector (C(update)).
      - Existing properties may be added/replaced depending on I(optype).
    type: dict

  start_time:
    description:
      - SDT start time. If omitted, defaults to the time the action is executed.
      - Format C(yyyy-MM-dd HH:mm) or C(yyyy-MM-dd HH:mm z) where C(z) is C(am) or C(pm).
    type: str
    default: ""

  end_time:
    description:
      - SDT end time. If omitted, I(duration) is used.
      - Format C(yyyy-MM-dd HH:mm) or C(yyyy-MM-dd HH:mm z).
    type: str
    default: ""

  duration:
    description:
      - SDT duration in minutes (used when I(end_time) is not provided).
    type: int
    default: 30

  comment:
    description:
      - SDT note/comment.
    type: str
    default: ""

  force_manage:
    description:
      - When true, if an C(update) targets a non-existent collector, the task may add/manage it.
    type: bool
    default: true
    choices: [true, false]

  optype:
    description: |-
      How to handle property updates for C(update).
      - C(replace): update existing properties or create if missing (default).
      - C(refresh): update existing and remove any not provided in this update.
      - C(add): create only if property does not already exist.
    type: str
    default: replace
    choices: ['refresh', 'replace', 'add']
'''

EXAMPLES = r'''
# Example of adding a collector
- name: Add Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Add LogicMonitor collector
      lm_collector:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        collector_group_name: "test group"
        device_group_full_path: "Devices by Type/Test Group"
        version: 29.107
        size: large

# Example of updating a collector
- name: Update Collector
  hosts: localhost
  tasks:
    - lm_collector:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1
        description: "localhost new"
        escalating_chain_name: "ansible chain"
        backup_collector_id: 1
        resend_collector_down_alert_interval: 60
        properties:  {
            "size": "medium"
        }
        optype: replace

# Example of removing a collector
- name: Remove Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Remove LogicMonitor collector
      lm_collector:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1

# Example of putting a collector in SDT
- name: SDT Collector
  hosts: localhost
  tasks:
    - name: Place LogicMonitor collector into Scheduled downtime (default is 30 min.)
      lm_collector:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        start_time: "1/1/2022 15:00"
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
    description: contain collector or sdt details
    returned: success
    type: dict
    sample: { "id": 4, "description": "new collector" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Collector updated successfully"
'''

import os
import platform
import sys

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import \
    LogicMonitorBaseModule

ID = "id"
DESCRIPTION = "description"
COLLECTOR_ID = "collectorId"
COLLECTOR_GROUP_ID = "collectorGroupId"
SPECIFIED_COLLECTOR_DEVICE_GROUP_ID = "specifiedCollectorDeviceGroupId"
BACKUP_AGENT_ID = "backupAgentId"
RESEND_IVAL = "resendIval"
ESCALATING_CHAIN_ID = "escalatingChainId"
CUSTOM_PROPERTIES = "customProperties"


class Collector(LogicMonitorBaseModule):

    def __init__(self):
        """ Initialize the the LogicMonitor Collector object """

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

        sizes = [
            "nano",
            "small",
            "medium",
            "large"
        ]

        module_args = dict(
            action=dict(required=True, choices=actions),
            company=dict(required=True),
            domain=dict(required=False, default="logicmonitor.com"),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            description=dict(required=False),
            install_path=dict(required=False, default="/usr/local/logicmonitor"),
            install_user=dict(required=False, default="logicmonitor"),
            collector_group_id=dict(required=False, type="int"),
            collector_group_name=dict(required=False),
            device_group_id=dict(required=False, type="int"),
            device_group_full_path=dict(required=False),
            platform=dict(required=False),
            version=dict(required=False),
            size=dict(required=False, default="small", choices=sizes),
            escalating_chain_id=dict(required=False, type="int"),
            escalating_chain_name=dict(required=False),
            backup_collector_id=dict(required=False, type="int"),
            backup_collector_description=dict(required=False),
            resend_collector_down_alert_interval=dict(required=False, type="int"),
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
        self.module.debug("Instantiating Collector object")

        self.id = self.params[self.ModuleFields.ID]
        self.description = self.params[self.ModuleFields.DESCRIPTION]
        self.install_path = self.process_field(self.params[self.ModuleFields.INSTALL_PATH], "/usr/local/logicmonitor")
        self.install_user = self.process_field(self.params[self.ModuleFields.INSTALL_USER], "logicmonitor")

        self.collector_group_id = self.params[self.ModuleFields.COLLECTOR_GROUP_ID]
        self.collector_group_name = self.params[self.ModuleFields.COLLECTOR_GROUP_NAME]
        self.device_group_id = self.params[self.ModuleFields.DEVICE_GROUP_ID]
        self.device_group_full_path = self.params[self.ModuleFields.DEVICE_GROUP_FULL_PATH]

        # the platform is temporary in order to test downloading in mac machines
        # customers will only be able to install collectors in Linux machines
        self.platform = platform.system().lower()
        if self.platform != "linux":
            self.platform = self.process_field(self.params[self.ModuleFields.PLATFORM]).lower()

        self.is_64bits = sys.maxsize > 2 ** 32
        self.version = self.params[self.ModuleFields.VERSION]
        if self.version is not None:
            self.version = self.version.strip().replace(".", "")
        self.size = self.params[self.ModuleFields.SIZE]
        self.start_time = self.process_field(self.params[self.ModuleFields.START_TIME])
        self.end_time = self.process_field(self.params[self.ModuleFields.END_TIME])
        self.duration = self.process_field(self.params[self.ModuleFields.DURATION], 30)
        self.comment = self.params[self.ModuleFields.COMMENT]
        self.escalating_chain_id = self.params[self.ModuleFields.ESCALATING_CHAIN_ID]
        self.escalating_chain_name = self.params[self.ModuleFields.ESCALATING_CHAIN_NAME]
        self.backup_collector_id = self.params[self.ModuleFields.BACKUP_COLLECTOR_ID]
        self.backup_collector_desc = self.params[self.ModuleFields.BACKUP_COLLECTOR_DESCRIPTION]
        self.resend_ival = self.params[self.ModuleFields.RESEND_IVAL]
        self.properties = self.params[self.ModuleFields.PROPERTIES]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        self.optype = self.params[self.ModuleFields.OPTYPE]
        # info contains collector JSON object (if it exists), None (if it doesn't exist), or an error message from the
        # API (if retrieval failed)
        self.info = self.collector_utils.get_collector_info(self.id, self.description, False)

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
            errmsg = ("Unexpected action \"" + str(
                self.module.params[self.ModuleFields.ACTION]) + "\" was specified.")
            self.fail(errmsg)
        self.exit_with_info()

    def add(self):
        """ Add LogicMonitor collector """
        self.module.debug("Running Collector.add...")
        if not self.success_response(self.info):
            response = self.add_to_account()
            message = "New collector successfully installed"
        else:
            self.id = self.info[self.ID]
            message = "Existing collector successfully installed"
            response = self.info
        installer_file_path = self.get_installer_binary()
        self.install(installer_file_path)
        self.additional_info = message
        self.result = self.get_basic_info_from_response(response)
        self.action_performed = "add"
        self.changed = True

    def add_to_account(self):
        """ Add a collector to a LogicMonitor account """
        self.module.debug("Running Collector.add_to_account...")

        if self.platform != "linux":
            self.fail("Error: LogicMonitor Collector must be installed on a Linux machine.")
        elif os.path.exists(self.install_path + "/agent"):
            self.fail("Collector already installed in " + self.install_path)
        else:
            data = {}
            if self.description:
                data[DESCRIPTION] = self.description

            if self.valid_id(self.collector_group_id) or self.collector_group_name is not None:
                data[COLLECTOR_GROUP_ID] = self.collector_group_utils.get_collector_group_id(self.collector_group_id,
                                                                                             self.collector_group_name)

            if self.valid_id(self.device_group_id) or self.device_group_full_path is not None:
                data[SPECIFIED_COLLECTOR_DEVICE_GROUP_ID] = \
                    self.device_group_utils.get_device_group_id(self.device_group_id, self.device_group_full_path)

            added_collector = self.add_collector_to_lm_account(data)
            self.id = added_collector[ID]
            return added_collector

    def add_collector_to_lm_account(self, data):
        """
        Add the collector to a LogicMonitor account

        :param data: JSON data associated with collector
        :return JSON-represented collector added to LM account
        """
        self.module.debug("Running Collector.add_collector_to_lm_account...")
        err_msg = "Failed to add collector to LogicMonitor account  \ndata: " + str(data)
        return self.rest_request(self.POST, self.COLLECTORS_BASE_URL, data, err_msg=err_msg)

    def get_installer_binary(self):
        """ Download the LogicMonitor collector installer binary & return it's filepath"""
        self.module.debug("Running Collector.get_installer_binary...")

        if not self.valid_id(self.id):
            self.fail("Collector downloading requires a collector ID greater than 0")

        arch = 64 if self.is_64bits else 32

        if self.check_mode:
            self.change = True
            self.exit()

        if not os.path.exists(self.install_path):
            self.module.run_command("mkdir -m755 " + self.install_path)

        try:
            installer_file_path = self.install_path + "/logicmonitorbootstrapx" + str(arch) + "_" + str(
                self.id) + ".bin"

            installer = self.download_collector_installer(self.id, arch, self.version, self.size)
            file = open(installer_file_path, "wb")
            file.write(bytes(installer))
            file.close()
            self.module.run_command("chmod +x " + installer_file_path)
            self.change = True
            return installer_file_path
        except Exception as e:
            self.fail(msg="Unable to open installer file for writing \nException: " + str(e))

    def download_collector_installer(self, id, arch, version, size):
        """
        Download the collector installer file

        :param id: the ID of the collector
        :param arch: the architecture of the device where download is occurring
        :param version: the version of the collector
        :param size: the size of the collector
        :return: binary representing the collector installer
        """
        self.module.debug("Running Collector.download_collector_installer...")
        if version:
            path_params = '?collectorVersion={version}&collectorSize={size}'.format(version=version, size=size)
        else:
            path_params = '?collectorSize={size}'.format(size=size)
        url = self.DOWNLOAD_COLLECTOR_URL.format(id=id, arch=str(arch))
        err_msg = "Failed to download collector installer file from LogicMonitor"
        return self.rest_request(self.GET, url, path_params=path_params, err_msg=err_msg)

    def install(self, installer_file_path):
        """ Execute the LogicMonitor installer if not already installed """
        self.module.debug("Running Collector.install...")
        install_command = installer_file_path + " -y -d " + self.install_path + " -u " + self.install_user
        ret_code, out, err = self.module.run_command(install_command)
        if ret_code != 0:
            self.fail(msg="Error: Unable to install collector: " + str(err))
        else:
            self.module.debug("Collector installed successfully")
            self.change = True

    def update(self):
        """ Update LogicMonitor collector used for monitoring """
        self.module.debug("Running Collector.update...")

        if self.success_response(self.info):
            # collector exists
            self.id = self.info[self.ID]
            data = self.build_collector_data()
            self.module.debug("Data: " + str(data))
            response = self.collector_utils.send_patch_request(self.id, data)

            self.additional_info = "Collector updated successfully"
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # collector doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def build_collector_data(self):
        self.module.debug("Running Collector.build_collector_data...")
        data = {}
        if self.description is not None:
            data[self.DESCRIPTION] = self.description
        if self.valid_id(self.collector_group_id) or self.collector_group_name is not None:
            data[COLLECTOR_GROUP_ID] = self.collector_group_utils.get_collector_group_id(self.collector_group_id,
                                                                                         self.collector_group_name)
        if self.escalating_chain_id == 0:
            data[ESCALATING_CHAIN_ID] = 0
        elif self.valid_id(self.escalating_chain_id) or self.escalating_chain_name is not None:
            data[ESCALATING_CHAIN_ID] = self.escalation_chain_utils.get_escalation_chain_id(self.escalating_chain_id,
                                                                                            self.escalating_chain_name)
        if self.backup_collector_id == 0:
            data[BACKUP_AGENT_ID] = 0
        elif self.valid_id(self.backup_collector_id) or self.backup_collector_desc is not None:
            data[BACKUP_AGENT_ID] = self.collector_utils.get_collector_id(self.backup_collector_id,
                                                                          self.backup_collector_desc)
        if self.resend_ival is not None:
            data[RESEND_IVAL] = self.resend_ival
        if self.properties is not None:
            data[CUSTOM_PROPERTIES] = self.build_properties(self.properties)
        return data

    def validate_update_fields(self):
        self.module.debug("Running Collector.validate_update_fields...")
        err_msg = "Invalid arguments - Updating a collector requires an existing collector id or description."
        if not self.valid_id(self.id) and self.description is None:
            self.fail(err_msg)

    def remove(self):
        """ Remove collector from LogicMonitor account and uninstall collector from the system """
        self.module.debug("Running Collector.remove...")
        self.remove_from_account()
        self.uninstall()
        self.action_performed = "remove"
        self.result = self.get_basic_info()
        self.changed = True
        self.additional_info = "Collector removed successfully"

    def remove_from_account(self):
        """ Delete collector from the associated LogicMonitor account """
        self.module.debug("Running Collector.remove_from_account...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        url = self.COLLECTORS_BASE_URL + "/" + str(self.id)
        err_msg = "Failed to remove collector " + str(self.id)
        self.rest_request(self.DELETE, url, err_msg=err_msg)
        self.module.debug("Collector successfully deleted from LogicMonitor account")

    def uninstall(self):
        """ Uninstall LogicMonitor collector from the system """
        self.module.debug("Running Collector.uninstall...")

        uninstaller_file = self.install_path + "/agent/bin/uninstall.sh"

        if os.path.isfile(uninstaller_file):
            if self.check_mode:
                self.change = True
                self.exit()

            ret_code, out, err = self.module.run_command(uninstaller_file)
            if ret_code != 0:
                self.fail("Error: Unable to uninstall collector: " + str(err))
            else:
                self.module.debug("Collector successfully uninstalled")
                self.change = True
        else:
            if not os.path.exists(self.install_path + "/agent"):
                self.fail("Unable to start uninstallation - no collector agent found in " + self.install_path + "")
            else:
                self.fail("Unable to start uninstallation - uninstaller file '" + uninstaller_file + "' not found")

    def validate_remove_fields(self):
        self.module.debug("Running Collector.validate_remove_fields...")
        err_msg = "Invalid arguments - Removing a collector requires an existing collector id or description."
        if not self.valid_id(self.id) and self.description is None:
            self.fail(err_msg)

    def sdt(self):
        """ Schedule down time for this collector """
        self.module.debug("Running Collector.sdt...")

        sdt_interval = self.get_sdt_interval(self.start_time, self.end_time, self.duration)

        data = {
            self.SDTFields.TYPE: self.SDTFields.COLLECTOR_SDT,
            self.SDTFields.SDT_TYPE: self.SDTFields.ONE_TIME,
            self.SDTFields.START_DATE_TIME: sdt_interval[0],
            self.SDTFields.END_DATE_TIME: sdt_interval[1],
            self.SDTFields.COMMENT: self.comment
        }
        self.update_sdt_data(data)

        err_msg = "Failed to SDT collector  \ndata: " + str(data)
        response = self.rest_request(self.POST, self.SDT_URL, data, err_msg=err_msg)
        self.additional_info = "Collector SDT successful"
        self.action_performed = "sdt"
        self.result = self.get_sdt_info_from_response(response)

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def update_sdt_data(self, data):
        """ Add data fields for collector SDTing """
        self.module.debug("Running Collector.update_sdt_data...")
        if self.valid_id(self.id) or self.description is not None:
            if self.success_response(self.info):
                data[COLLECTOR_ID] = self.info[self.ID]
            else:
                self.handle_error_response()
        else:
            self.fail(
                "Invalid arguments - This SDT action requires the collector id (greater than 0) or description.")

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " collector"
        if not self.info:
            # collector doesn't exist
            self.fail(err_msg_template + " - Collector doesn't exist")
        else:
            # err msg received from LM not related to collector existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID), DESCRIPTION: self.info.get(DESCRIPTION)
                }

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID), DESCRIPTION: response.get(DESCRIPTION)
                }

    def get_sdt_info_from_response(self, response):
        return {self.ModuleFields.START_TIME: response.get(self.SDTFields.START_DATE_TIME_ON_LOCAL),
                self.ModuleFields.END_TIME: response.get(self.SDTFields.END_DATE_TIME_ON_LOCAL),
                self.ModuleFields.DURATION: response.get(self.ModuleFields.DURATION),
                self.SDTFields.SDT_ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.COLLECTOR_ID: response.get(COLLECTOR_ID)}


def main():
    module = Collector()
    module.run()


if __name__ == "__main__":
    main()

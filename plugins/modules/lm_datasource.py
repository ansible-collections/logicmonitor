#!/usr/bin/python

# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: lm_datasource

short_description: LogicMonitor Datasource Ansible module for managing device datasources.

version_added: "1.0.0"

author:
    - Carlos Alvarenga (@cealvar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages device datasources within your LogicMonitor account (i.e. sdt).

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
            - SDT = Schedule downtime for a device datasource in your LogicMonitor account.
        required: true
        type: str
        choices: ["sdt"]
    id:
        description:
            - ID of the device datasource to target.
            - Required for action=sdt if datasource name isn't provided.
        type: int
    name:
        description:
            - Name of the device datasource to target.
            - Required for action=sdt if datasource id isn't provided.
        type: str
    device_id:
        description:
            - ID of device (containing datasource) to target.
            - Required for action=sdt if the following are true ...
                (1) id of datasource isn't provided
                (2) name of datasource is provided
                (3) device_display_name isn't provided
                (4) device_hostname isn't provided.
        type: int
    device_display_name:
        description:
            - display name of device (containing datasource) to target.
            - Required for action=sdt if the following are true ...
                (1) id of datasource isn't provided
                (2) name of datasource is provided
                (3) device_id isn't provided
                (4) device_hostname isn't provided.
            - Required for device SDT if both device ID and name aren't provided.
        type: str
    device_hostname:
        description:
            - hostname (name) of device (containing datasource) to target.
            - Required for action=sdt if the following are true ...
                (1) id of datasource isn't provided
                (2) name of datasource is provided
                (4) device_id isn't provided
                (3) device_display_name isn't provided.
        type: str
'''

EXAMPLES = r'''
# Example of putting a device datasource in SDT
- name: SDT Datasource
  hosts: localhost
  tasks:
    - name: Place LogicMonitor datasource into Scheduled downtime (default is 30 min.)
      logicmonitor:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "ping"
        device_display_name: "127.0.0.1_collector_1"
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
    description: contain datasource or sdt details
    returned: success
    type: dict
    sample: { "datasource_id": 4, "datasource_name": "Host Status", "duration": 5,
            "end_time": "2022-09-20 16:55:07 IST", "start_time": "2022-09-20 16:50:07 IST", "std_id": "S_25"}
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: std
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Datasource SDT successful"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

DEVICE_ID = "deviceId"
DEVICE_DISPLAY_NAME = "deviceDisplayName"
DEVICE_DATASOURCE_ID = "deviceDataSourceId"
DATASOURCE_NAME = "dataSourceName"


class Datasource(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize the the LogicMonitor Datasource Datasource object """

        self.changed = False
        self.action_performed = "None"
        self.result = None
        self.additional_info = ""
        actions = [
            self.SDT
        ]

        module_args = dict(
            action=dict(required=True, choices=actions),
            company=dict(required=True),
            domain=dict(required=False, default="logicmonitor.com"),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            name=dict(required=False),
            device_id=dict(required=False, type="int"),
            device_display_name=dict(required=False),
            device_hostname=dict(required=False),
            start_time=dict(required=False, default=""),
            end_time=dict(required=False, default=""),
            duration=dict(required=False, default=30, type="int"),
            comment=dict(required=False, default="")
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating Device Datasource object")

        self.id = self.params[self.ModuleFields.ID]
        self.name = self.params[self.ModuleFields.NAME]
        self.device_id = self.params[self.ModuleFields.DEVICE_ID]
        self.device_display_name = self.params[self.ModuleFields.DEVICE_DISPLAY_NAME]
        self.device_hostname = self.params[self.ModuleFields.DEVICE_HOSTNAME]
        self.start_time = self.process_field(self.params[self.ModuleFields.START_TIME])
        self.end_time = self.process_field(self.params[self.ModuleFields.END_TIME])
        self.duration = self.process_field(self.params[self.ModuleFields.DURATION], 30)
        self.comment = self.params[self.ModuleFields.COMMENT]

    def run(self):
        """ Run module to perform action requested by the user """
        self.module.debug("Running module...")
        action = self.module.params[self.ModuleFields.ACTION]
        if action == self.SDT:
            self.sdt()
        else:
            errmsg = ("Unexpected action \"" + str(self.module.params[self.ModuleFields.ACTION]) + "\" was specified.")
            self.fail(errmsg)

        self.exit_with_info()

    def get_device_datasource_by_id(self, datasource_id, device_id):
        """ Retrieve a LogicMonitor device datasource via it's ID

        :param datasource_id: the ID of the datasource queried
        :param device_id: the ID of the device associated with the datasource being queried
        :return: JSON object representing the device datasource
        """
        self.module.debug("Running Datasource.get_device_datasource_by_id...")

        device_datasource = None
        if self.valid_id(datasource_id) and self.valid_id(device_id):
            url = self.DEVICE_DATASOURCES_BASE_URL.format(device_id=device_id) + "/" + str(datasource_id)
            err_msg = "Failed to retrieve device datasource by ID"
            device_datasource = self.rest_request(self.GET, url, err_msg=err_msg)
        if not device_datasource:
            self.fail("Device datasource '" + str(datasource_id) + "' doesn't exist")
        return device_datasource

    def get_device_datasource_by_name(self, datasource_name, device_id="", device_display_name="", device_hostname=""):
        """ Retrieve a LogicMonitor device datasource via the datasource name and its device's ID

        :param datasource_name: the name of the datasource queried
        :param device_id: the ID of the device associated with the datasource queried
        :param device_hostname: the name (i.e. hostname) of the device associated with the datasource queried
        :param device_display_name: the displayName of the device associated with the datasource queried
        :return: JSON object representing the device datasource or None if it isn't found
        """
        self.module.debug("Running Datasource.get_device_datasource_by_name...")

        if datasource_name:
            device_id = self.device_utils.get_device_id(device_id, device_display_name, device_hostname)
            url = self.DEVICE_DATASOURCES_BASE_URL.format(device_id=device_id)
            query_filter = 'dataSourceName:"{dn}"'.format(dn=datasource_name)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve device datasources by name"
            response = self.rest_request(self.GET, url, query_params=query_params, err_msg=err_msg)

            num_items = response[self.TOTAL]
            if num_items > 0:
                return response[self.ITEMS][0]
        self.fail("Datasource '" + datasource_name + "' doesn't exist")

    def sdt(self):
        """ Schedule down time for this datasource """
        self.module.debug("Running Datasource.sdt...")

        sdt_interval = self.get_sdt_interval(self.start_time, self.end_time, self.duration)

        data = {
            self.SDTFields.TYPE: self.SDTFields.DEVICE_DATASOURCE_SDT,
            self.SDTFields.SDT_TYPE: self.SDTFields.ONE_TIME,
            self.SDTFields.START_DATE_TIME: sdt_interval[0],
            self.SDTFields.END_DATE_TIME: sdt_interval[1],
            self.SDTFields.COMMENT: self.comment
        }
        self.update_sdt_data(data)

        err_msg = "Failed to SDT device datasource \ndata: " + str(data)
        response = self.rest_request(self.POST, self.SDT_URL, data, err_msg=err_msg)
        self.action_performed = "sdt"
        self.additional_info = "Website check SDT successful"
        self.result = self.get_sdt_info_from_response(response)

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit(changed=True)

    def update_sdt_data(self, data):
        """ Add data fields for device datasource SDTing """
        self.module.debug("Running Datasource.update_sdt_data...")

        err_msg = "Invalid arguments - This SDT action requires one of the following device datasource fields: " \
                  "(1) id (greater than 0) OR " \
                  "(2) name and either device_id (greater than 0), device_hostname, or device_display_name"
        if self.valid_id(self.id):
            data[DEVICE_DATASOURCE_ID] = self.id
        elif self.name:
            data[DATASOURCE_NAME] = self.name.strip()
            if self.valid_id(self.device_id) or self.device_display_name or self.device_hostname:
                data[DEVICE_ID] = self.device_utils.get_device_id(self.device_id, self.device_display_name,
                                                                  self.device_hostname)
            else:
                self.fail(err_msg)
        else:
            self.fail(err_msg)

    def get_sdt_info_from_response(self, response):
        return {self.ModuleFields.START_TIME: response.get(self.SDTFields.START_DATE_TIME_ON_LOCAL),
                self.ModuleFields.END_TIME: response.get(self.SDTFields.END_DATE_TIME_ON_LOCAL),
                self.ModuleFields.DURATION: response.get(self.ModuleFields.DURATION),
                self.SDTFields.SDT_ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.DATASOURCE_NAME: response.get(DATASOURCE_NAME),
                self.ModuleFields.DATASOURCE_ID: response.get(DEVICE_DATASOURCE_ID)}


def main():
    module = Datasource()
    module.run()


if __name__ == "__main__":
    main()

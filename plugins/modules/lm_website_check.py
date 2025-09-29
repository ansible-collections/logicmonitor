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
module: lm_website_check

short_description: LogicMonitor Website Check Ansible module for managing website checks.

version_added: "1.2.0"

author:
    - Gunjan Kumar (@gunjan)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages website checks within your LogicMonitor account (i.e. sdt a ping or web check).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options
    - logicmonitor.integration.lm_sdt_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the website check (ping or web check).
            - SDT = Schedule downtime for a website check in your LogicMonitor account.
        required: true
        type: str
        choices: ["sdt"]
    website_check_id:
        description:
            - ID of the website check (ping or web check) to target.
            - Required for action=sdt if website check name isn't provided.
        type: int
    website_check_name:
        description:
            - Name of the website check (ping or web check) to target.
            - Required for action=sdt if website check id isn't provided.
        type: str
    checkpoint_id:
        description:
            - ID of the checkpoint location you want to put in SDT.
            - Required for action=sdt if you want to apply SDT at specific location
                and checkpoint name isn't provided.
            - If no checkpoint (id or name) is provided it will put the whole website check in SDT.
        type: int
    checkpoint_name:
        description:
            - Name of the checkpoint location you want to put in SDT.
            - Required for action=sdt if you want to apply SDT at specific location
                and checkpoint id isn't provided.
            - If no checkpoint (id or name) is provided it will put the whole website check in SDT.
        type: str
'''

EXAMPLES = r'''
# Example of putting a website check (ping or web check) in SDT
- name: SDT Website check
  hosts: localhost
  tasks:
    - name: Place LogicMonitor website check (ping or web check) into Scheduled downtime.
      logicmonitor:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        website_check_id: 1
        start_time: "1/10/2022 15:00"
        duration: 60

# Example of putting a website check (ping or web check) in SDT from different locations
- name: SDT Website check by locations
  hosts: localhost
  tasks:
    - name: Place LogicMonitor website check (ping or web check) into Scheduled downtime.
      logicmonitor:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        website_check_id: 1
        start_time: "1/10/2022 15:00"
        duration: 60
        checkpoint_name: "{{item}}"
      loop:
        - Europe - Dublin
        - Asia - Singapore
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
    description: contain website check or sdt details
    returned: success
    type: dict
    sample: { "website_check_id": 4, "website_check_name": "test", "duration": 5,
            "end_time": "2022-09-20 16:55:07 IST", "start_time": "2022-09-20 16:50:07 IST", "std_id": "D_17"}
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: std
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Website check SDT successful"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

WEBSITE_ID = "websiteId"
WEBSITE_NAME = "websiteName"
CHECKPOINT_ID = "checkpointId"
CHECKPOINTS = "checkpoints"
ID = "id"
NAME = "name"
GEO_INFO = "geoInfo"


class WebsiteCheck(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize  the LogicMonitor Website Check object """

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
            start_time=dict(required=False, default=""),
            end_time=dict(required=False, default=""),
            duration=dict(required=False, default=30, type="int"),
            comment=dict(required=False, default=""),
            website_check_id=dict(required=False, type="int"),
            website_check_name=dict(required=False, type="str"),
            checkpoint_id=dict(required=False, type="int"),
            checkpoint_name=dict(required=False, type="str")
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating website check object")

        self.start_time = self.process_field(self.params[self.ModuleFields.START_TIME])
        self.end_time = self.process_field(self.params[self.ModuleFields.END_TIME])
        self.duration = self.process_field(self.params[self.ModuleFields.DURATION], 30)
        self.comment = self.params[self.ModuleFields.COMMENT]
        self.website_check_id = self.params[self.ModuleFields.WEBSITE_CHECK_ID]
        self.website_check_name = self.params[self.ModuleFields.WEBSITE_CHECK_NAME]
        self.checkpoint_id = self.params[self.ModuleFields.CHECKPOINT_ID]
        self.checkpoint_name = self.params[self.ModuleFields.CHECKPOINT_NAME]

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

    def sdt(self):
        """ Schedule downtime for this website check """
        self.module.debug("Running WebsiteCheck.sdt...")

        sdt_interval = self.get_sdt_interval(self.start_time, self.end_time, self.duration)

        data = {
            self.SDTFields.TYPE: self.SDTFields.WEBSITE_SDT,
            self.SDTFields.SDT_TYPE: self.SDTFields.ONE_TIME,
            self.SDTFields.START_DATE_TIME: sdt_interval[0],
            self.SDTFields.END_DATE_TIME: sdt_interval[1],
            self.SDTFields.COMMENT: self.comment,

        }

        if self.checkpoint_id or self.checkpoint_name:
            self.update_sdt_data_location(data)
        self.update_sdt_data(data)

        err_msg = "Failed to SDT website check \ndata: " + str(data)
        response = self.rest_request(self.POST, self.SDT_URL, data, err_msg=err_msg)
        self.action_performed = "sdt"
        self.additional_info = "Website check SDT successful"
        self.result = self.get_sdt_info_from_response(response)

        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit(changed=True)

    def update_sdt_data_location(self, data):
        """ Add data fields for website check SDTing """
        self.module.debug("Running WebsiteCheck.update_sdt_data...")
        err_msg = "Location not found \n Available locations : "
        data[self.SDTFields.TYPE] = self.SDTFields.WEBSITE_CHECKPOINT_SDT
        data[CHECKPOINT_ID] = self.get_checkpoint_id()

    def get_checkpoint_id(self):
        self.info = self.website_check_utils.get_website_check_info(self.website_check_id, self.website_check_name, True)
        checkpoints = []
        for temp in self.info[CHECKPOINTS]:
            temp_checkpoint = {ID: temp[ID], NAME: temp[GEO_INFO]}
            checkpoints.append(temp_checkpoint)
        valid = False
        checkpoint_id = -1

        if self.checkpoint_id is not None:
            for checkpoint in checkpoints:
                if checkpoint[ID] == self.checkpoint_id:
                    valid = True
                    checkpoint_id = checkpoint[ID]
                    break
            if not valid:
                self.fail("Checkpoint does not exist id - '" + str(self.checkpoint_id) + "' "
                          "\n Available checkpoints - " + str(checkpoints))

        if not valid and self.checkpoint_name is not None:
            for checkpoint in checkpoints:
                if checkpoint[NAME] == self.checkpoint_name:
                    valid = True
                    checkpoint_id = checkpoint[ID]
                    break
            if not valid:
                self.fail("Checkpoint does not exist name - '" + self.checkpoint_name + "' "
                          "\n Available checkpoints - " + str(checkpoints))
        return checkpoint_id

    def update_sdt_data(self, data):
        """ Add data fields for website check SDTing """
        self.module.debug("Running WebsiteCheck.update_sdt_data...")

        err_msg = "Invalid arguments - This SDT action requires one of the following website check detail : " \
                  "(1) website_check_id (greater than 0) OR " \
                  "(2) website_check_name"
        if self.valid_id(self.website_check_id):
            data[WEBSITE_ID] = self.website_check_id
        elif self.website_check_name:
            data[WEBSITE_NAME] = self.website_check_name.strip()
            if self.website_check_name:
                data[WEBSITE_NAME] = self.website_check_name
            else:
                self.fail(err_msg)
        else:
            self.fail(err_msg)

    def get_sdt_info_from_response(self, response):
        return {self.ModuleFields.START_TIME: response.get(self.SDTFields.START_DATE_TIME_ON_LOCAL),
                self.ModuleFields.END_TIME: response.get(self.SDTFields.END_DATE_TIME_ON_LOCAL),
                self.ModuleFields.DURATION: response.get(self.ModuleFields.DURATION),
                self.SDTFields.SDT_ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.WEBSITE_CHECK_NAME: response.get(WEBSITE_NAME),
                self.ModuleFields.WEBSITE_CHECK_ID: response.get(WEBSITE_ID)}


def main():
    module = WebsiteCheck()
    module.run()


if __name__ == "__main__":
    main()

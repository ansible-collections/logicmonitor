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
module: lm_escalation_chain

short_description: LogicMonitor Escalation Chain Ansible module for managing escalation chain.

version_added: "1.2.0"

author:
    - Gunjan Kumar (@gunjan)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages escalation chain within your LogicMonitor account (i.e. add, update, remove).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    action:
        description:
            - The action you wish to perform on the escalation chain.
            - Add = Add a escalation chain to your LogicMonitor account.
            - Update = rate limit, destination / recipient etc for a escalation chain in your LogicMonitor account.
            - Remove = Remove a escalation chain from your LogicMonitor account.
        required: true
        type: str
        choices: ["add", "update", "remove"]
    id:
        description:
            - ID of the escalation chain to target.
            - Required for managing escalation chain (action=update and action=remove) if name isn't provided.
        type: int
    name:
        description:
            - The name of the escalation chain to target.
            - Required for managing escalation chain (action=add).
            - Required for managing escalation chain (action=update and action=remove) if name isn't provided.
        type: str
    enable_throttling:
        description:
            - A boolean flag to enable/disable alert throttling.
            - Required for managing escalation chain (action=add).
            - Optional for managing escalation chain (action=update).
        type: bool
        choices: [True, False]
    rate_limit_alerts:
        description:
            - The maximum number of alert notifications that can be delivered during the Rate Limit Period.
            - Note that re-sent alert notifications count towards this number.
            - Required for managing escalation chain (action=add and action=update) if enable_throttling is set to true.
        type: int
    rate_limit_period:
        description:
            - The period (minutes) over which max number of alerts (specified in rate_limit_alerts) can be sent out.
            - Required for managing escalation chain (action=add and action=update) if enable_throttling is set to true.
        type: int
    description:
        description:
            - Description of escalation chain.
            - Optional for managing escalation chain (action=add or action=update).
        type: str
    destinations:
        description:
            - Destinations consists of ordered list of stages.
            - Stages consist of one or more recipients that alert notifications will be routed to.
            - Required for managing escalation chain (action=add).
            - Optional for managing escalation chain (action=update).
            - Recipient is a JSON object pointing to any one of the following...
              (1) integration - send alerts to integrations (sms, email, pagerduty, autotask, etc...)
                  required properties
                    name - name of the integration
                    user - logicmonitor username
                  Note in case of email, sms and voice name would be type (ie for email name would be email)
              (2) arbitrary emails - send alert to the given email address
                  required properties
                    name - name must be "arbitrary-email"
                    address - email address
              (3) recipient group - send alert to a recipient group
                  required properties
                    name - name must be "group"
                    group-name - name of the group
        type: list
        elements: list
    cc_destinations:
        description:
            - cc destination is a list of recipients
            - Recipients in cc will receive all notifications sent to every stage in the escalation chain.
            - Optional for managing escalation chain (action=add or action=update).
            - Recipient is a JSON object pointing to any one of the following...
              (1) integration - send alerts to integrations (sms, email, pagerduty, autotask, etc...)
                  required properties
                    name - name of the integration
                    user - logicmonitor username
                  Note in case of email, sms and voice name would be type (ie for email name would be email)
              (2) arbitrary emails - send alert to the given email address
                  required properties
                    name - name must be "arbitrary-email"
                    address - email address
              (3) recipient group - send alert to a recipient group
                  required properties
                    name - name must be "group"
                    group-name - name of the group
            - Optional for managing escalation chain (action=add or action=update).
        type: list
        elements: dict
    force_manage:
        description:
            - A boolean flag to enable/disable the feature to ...
              (1) update a escalation chain when the initial action=add because the chain exists or
              (2) add a escalation chain when the initial action=update because the chain doesn't exist.
            - Optional for managing escalation chain (action=add or action=update).
        type: bool
        default: True
        choices: [True, False]
'''

EXAMPLES = r'''
# Example of adding an escalation chain
- name: Add Escalation Chain
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
        enable_throttling: True
        rate_limit_period: 22
        rate_limit_alerts: 33
        description: added from ansible
        destinations: [
          [
            {"name":"ConnectWise Integration-clone", "user":"john.doe@logicmonitor.com"},
            {"name":"group", "group-name":"test-group"},
            {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"}
          ],
          [
            {"name":"email","user":"john.doe@logicmonitor.com" },
            {"name":"voice","user":"john.doe@logicmonitor.com" }
           ]
        ]
        cc_destinations: [
          {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"},
          {"name":"arbitrary-email", "address":"john.doe@google.com"},
          {"name":"Autotask Integration -New", "user":"john.doe@logicmonitor.com"}
        ]

# Example of updating an escalation chain
- name: Update Escalation Chain
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
        enable_throttling: false
        rate_limit_period: 22
        rate_limit_alerts: 33
        description: added from ansible
        destinations: [
          [
            {"name":"ConnectWise Integration-clone", "user":"john.doe@logicmonitor.com"},
            {"name":"group", "group-name":"test-group"},
            {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"}
          ],
          [
            {"name":"email","user":"john.doe@logicmonitor.com" },
            {"name":"voice","user":"john.doe@logicmonitor.com" }
           ]
        ]

# Example of removing an escalation chain
- name: Remove Escalation Chain
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
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
    sample: { "id": 4, "name": "new-chain" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Escalation Chain updated successfully"
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule


class EscalationChain(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize  the LogicMonitor Escalation Chain object """

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
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            enable_throttling=dict(required=False, type="bool", choices=[True, False]),
            rate_limit_alerts=dict(required=False, type='int'),
            rate_limit_period=dict(required=False, type='int'),
            cc_destinations=dict(required=False, type="list", elements="dict"),
            destinations=dict(required=False, type="list", elements="list"),
            force_manage=dict(required=False, type="bool", default=True, choices=[True, False])
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating Escalation Chain object")

        self.id = self.params[self.ModuleFields.ID]
        self.name = self.params[self.ModuleFields.NAME]
        self.description = self.params[self.ModuleFields.DESCRIPTION]
        self.enable_throttling = self.params[self.ModuleFields.ENABLE_THROTTLING]
        self.rate_limit_alerts = self.params[self.ModuleFields.RATE_LIMIT_ALERTS]
        self.rate_limit_period = self.params[self.ModuleFields.RATE_LIMIT_PERIOD]
        self.cc_destinations = self.params[self.ModuleFields.CC_DESTINATIONS]
        self.destinations = self.params[self.ModuleFields.DESTINATIONS]
        self.force_manage = self.params[self.ModuleFields.FORCE_MANAGE]
        # info contains escalation chain JSON object (if it exists), None (if it doesn't exist), or an error message
        # from the API (if retrieval failed)
        self.info = self.escalation_chain_utils.get_escalation_chain_info(self.id, self.name, False)

    def run(self):
        """ Run module to perform action requested by the user """
        self.module.debug("Running module...")
        action = self.module.params[self.ModuleFields.ACTION]
        # self.fail(msg=self.module)
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
        """ Add Escalation Chain in your LogicMonitor account """
        self.module.debug("Running EscalationChain.add...")

        if self.success_response(self.info):
            # chain exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add escalation chain - Escalation Chain already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # chain doesn't exist
                data = self.build_escalation_chain_data()
                self.module.debug("Data: " + str(data))
                response = self.escalation_chain_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Escalation Chain added successfully"

                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to escalation chain existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor Escalation Chain used for monitoring """
        self.module.debug("Running EscalationChain.update...")

        if self.success_response(self.info):
            # chain exists
            self.id = self.info[self.ID]
            self.validate_update_fields()
            data = self.build_escalation_chain_data()
            # self.fail(msg=data)
            self.module.debug("Data: " + str(data))
            response = self.escalation_chain_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Escalation Chain updated successfully"

            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # chain doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def remove(self):
        """ Remove this Escalation Chain from your LogicMonitor account """
        self.module.debug("Running EscalationChain.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        self.escalation_chain_utils.send_delete_request(self.id)
        self.action_performed = "remove"
        self.additional_info = "Escalation Chain removed successfully"
        self.result = self.get_basic_info()
        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def validate_add_fields(self):
        self.module.debug("Running EscalationChain.validate_add_fields...")
        if not self.name:
            self.fail("Invalid arguments - Adding an escalation chain requires a unique name.")
        if self.enable_throttling is None:
            self.fail("Invalid arguments - Adding an escalation chain requires enable_throttling.")
        elif self.enable_throttling is True:
            if not self.rate_limit_alerts:
                self.fail("Invalid arguments - rate_limit_alerts is required when enable_throttling is set to true.")
            if not self.rate_limit_period:
                self.fail("Invalid arguments - rate_limit_period is required when enable_throttling is set to true.")
        if not self.destinations:
            self.fail("Invalid arguments - Adding an escalation chain requires destinations.")

    def validate_update_fields(self):
        self.module.debug("Running EscalationChain.validate_update_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Updating an escalation chain requires an existing escalation chain id or "
                      "name.")
        if self.enable_throttling is True:
            if not self.rate_limit_alerts:
                self.fail("Invalid arguments - rate_limit_alerts is required when enable_throttling is set to true.")
            if not self.rate_limit_period:
                self.fail("Invalid arguments - rate_limit_period is required when enable_throttling is set to true.")

    def validate_remove_fields(self):
        self.module.debug("Running EscalationChain.validate_remove_fields...")
        if not self.valid_id(self.id) and self.name is None:
            self.fail("Invalid arguments - Removing an escalation chain requires an existing escalation chain id or "
                      "name.")

    def build_escalation_chain_data(self):
        self.module.debug("Running EscalationChain.build_escalation_chain_data...")
        data = {}
        if self.name is not None:
            data[self.ESCALATIONCHAINFields.NAME] = self.name
        if self.enable_throttling is not None:
            data[self.ESCALATIONCHAINFields.ENABLE_THROTTLING] = self.enable_throttling
        if self.rate_limit_alerts is not None:
            data[self.ESCALATIONCHAINFields.THROTTLING_ALERTS] = self.rate_limit_alerts
        if self.rate_limit_period is not None:
            data[self.ESCALATIONCHAINFields.THROTTLING_PERIOD] = self.rate_limit_period
        if self.cc_destinations is not None:
            data[self.ESCALATIONCHAINFields.CC_DESTINATIONS] = self.process_cc(self.cc_destinations)
        if self.destinations is not None:
            data[self.ESCALATIONCHAINFields.DESTINATIONS] = self.process_destinations(self.destinations)
        if self.description is not None:
            data[self.ESCALATIONCHAINFields.DESCRIPTION] = self.description
        return data

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " escalation chain"
        if not self.info:
            # escalation chain doesn't exist
            self.fail(err_msg_template + " - Escalation chain doesn't exist")
        else:
            # err msg received from LM not related to escalation chain existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def process_destinations(self, destinations):
        result = []
        destination = {"type": "single"}

        stages = []
        for stage in destinations:
            recipients = []
            for recipient in stage:
                recipient_obj = self.process_recipient(recipient)
                recipients.append(recipient_obj)
            stages.append(recipients)
        destination["stages"] = stages
        result.append(destination)
        return result

    def process_recipient(self, recipient):
        if recipient["name"] == "arbitrary-email":
            if "address" not in recipient:
                self.fail("Invalid arguments - address required for arbitrary-email recipient.")
            recipient_obj = {"type": "ARBITRARY",
                             "method": "email",
                             "addr": recipient["address"],
                             "contact": ""}
        elif recipient["name"] == "group":
            if "group-name" not in recipient:
                self.fail("Invalid arguments - group-name required for group recipient.")
            recipient_obj = self.recipient_utils.get_recipient_info(None, recipient["group-name"])
            recipient_obj["contact"] = ""
        else:
            if recipient["name"] is None or recipient["user"] is None:
                self.fail("Invalid arguments - name and user required for recipient.")
            recipient_obj = self.recipient_utils.get_recipient_info(recipient["name"], recipient["user"])
            recipient_obj["contact"] = ""
        return recipient_obj

    def process_cc(self, cc):
        result = []
        for recipient in cc:
            recipient_obj = self.process_recipient(recipient)
            result.append(recipient_obj)
        return result

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: self.info.get(self.ModuleFields.NAME)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.NAME: response.get(self.ModuleFields.NAME)}


def main():
    module = EscalationChain()
    module.run()


if __name__ == "__main__":
    main()

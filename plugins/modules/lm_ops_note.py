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
module: lm_ops_note

short_description: LogicMonitor Ops Note Ansible module for managing ops notes.

version_added: "2.1.0"

author:
    - Steven Villardi (@stevevillardi)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages ops notes within your LogicMonitor account (i.e. add, update, remove).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account

options:
    
'''

EXAMPLES = r'''
# Example of adding a ops note
- name: Add Ops Note
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Ops Note
      lm_ops_note:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        note: "This is a test note"
        tags: ["tag1", "tag2"]
        scopes: []
        happened_on_in_seconds: 1714857600

# Example of updating a ops note
- name: Update Ops Note
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Ops Note
      lm_ops_note:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
        note: "This is a test note"
        tags: ["tag1", "tag2"]
        scopes: []


# Example of removing a ops note
- name: Remove Ops Note
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Ops Note
      lm_ops_note:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
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
    description: contain ops note details
    returned: success
    type: dict
    sample: { "id": 4, "name": "note_1" }
action_performed:
    returned: success
    description: a string describing which action was performed
    type: str
    sample: add
addition_info:
    returned: success
    description: any additional detail related to the action
    type: str
    sample: "Ops Note updated successfully"
'''
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import LogicMonitorBaseModule

class OpsNote(LogicMonitorBaseModule):
    def __init__(self):
        """ Initialize  the LogicMonitor Ops Note object """

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
            id=dict(required=False, type="str"),
            note=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="str"),
            scopes=dict(required=False, type="list", elements="str"),
            scope_type=dict(required=False, type="str", choices=["device", "deviceGroup", "website"]),
            note_time=dict(required=False, type="str")
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating Ops Note object")

        self.id = self.params[self.ModuleFields.ID]
        self.note = self.params[self.ModuleFields.NOTE]
        self.tags = self.process_tags(self.params[self.ModuleFields.TAGS])
        self.scope_type = self.params[self.ModuleFields.SCOPE_TYPE]
        self.scopes = self.process_scopes(self.params[self.ModuleFields.SCOPES], self.scope_type)
        self.note_time = self.params[self.ModuleFields.NOTE_TIME]
        # info contains ops note JSON object (if it exists), None (if it doesn't exist), or an error message from
        # the API (if retrieval failed)
        self.info = self.ops_note_utils.get_ops_note_info(self.id, False)

    def process_tags(self, tags):
        """ Trim leading/trailing spaces from each element of the tags list  """
        self.module.debug("Running OpsNote,process_tags...")
        new_tags = None
        if tags is not None:
            new_tags = []
            for tag in tags:
                new_tags.append({"name": tag.strip()})
        return new_tags
    
    def process_scopes(self, scopes, scope_type):
        """ Trim leading/trailing spaces from each element of the scopes list  """
        self.module.debug("Running OpsNote,process_scopes...")
        new_scopes = None
        if scopes is not None:
            new_scopes = []
            for scope in scopes:
                if scope_type == "device":
                    new_scopes.append({"type": "device", "groupId": "0", "deviceId": scope.strip()})
                elif scope_type == "deviceGroup":
                    new_scopes.append({"type": "deviceGroup", "groupId": scope.strip()})
                elif scope_type == "website":
                    new_scopes.append({"type": "website", "groupId": "0", "websiteId": scope.strip()})
        return new_scopes

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
        """ Add Ops Note in your LogicMonitor account """
        self.module.debug("Running OpsNote.add...")

        if self.success_response(self.info):
            # ops note exists
            if self.force_manage:
                self.update()
            else:
                self.fail("Failed to add ops note - Ops note already exists")
        else:
            self.validate_add_fields()
            if not self.info:
                # ops note doesn't exist
                data = self.build_ops_note_data()
                self.module.debug("Data: " + str(data))
                response = self.ops_note_utils.send_create_request(data)
                self.result = self.get_basic_info_from_response(response)
                self.action_performed = "add"
                self.additional_info = "Ops Note added successfully"
                self.module.debug("System changed")
                self.changed = True
                if self.check_mode:
                    self.exit()
            else:
                # err msg received from LM not related to ops note existence
                self.handle_error_response()

    def update(self):
        """ Update LogicMonitor ops note """
        self.module.debug("Running OpsNote.update...")

        if self.success_response(self.info):
            # ops note exists
            self.id = self.info[self.ID]
            data = self.build_ops_note_data()
            self.module.debug("Data: " + str(data))
            response = self.ops_note_utils.send_patch_request(self.id, data)
            self.result = self.get_basic_info_from_response(response)
            self.action_performed = "update"
            self.additional_info = "Ops Note updated successfully"

            self.module.debug("System changed")
            self.changed = True
            if self.check_mode:
                self.exit()
        else:
            self.validate_update_fields()
            if not self.info and self.force_manage:
                # ops note doesn't exist
                self.add()
            else:
                self.handle_error_response()

    def remove(self):
        """ Remove this ops note from your LogicMonitor account """
        self.module.debug("Running OpsNote.remove...")

        if self.success_response(self.info):
            self.id = self.info[self.ID]
        else:
            self.validate_remove_fields()
            self.handle_error_response()

        self.ops_note_utils.send_delete_request(self.id)
        self.action_performed = "remove"
        self.additional_info = "Ops Note removed successfully"
        self.result = self.get_basic_info()
        self.module.debug("System changed")
        self.changed = True
        if self.check_mode:
            self.exit()

    def validate_add_fields(self):
        self.module.debug("Running OpsNote.validate_add_fields...")
        if not self.note:
            self.fail("Invalid arguments - Adding a ops note requires a note.")

    def validate_update_fields(self):
        self.module.debug("Running OpsNote.validate_update_fields...")
        if self.id is not None:
            self.fail("Invalid arguments - Updating a ops note requires an existing ops note id.")

    def validate_remove_fields(self):
        self.module.debug("Running OpsNote.validate_remove_fields...")
        if self.id is not None:
            self.fail("Invalid arguments - Removing a ops note requires an existing ops note id.")

    def build_ops_note_data(self):
        self.module.debug("Running OpsNote.build_ops_note_data...")
        data = {}
        if self.note is not None:
            data[self.OpsNoteFields.NOTE] = self.note
        if self.tags is not None:
            data[self.OpsNoteFields.OPS_NOTE_TAGS] = self.tags
        if self.scopes is not None:
            data[self.OpsNoteFields.OPS_NOTE_SCOPES] = self.scopes
        if self.note_time is not None:
            data[self.OpsNoteFields.OPS_NOTE_HAPPENED_ON_IN_SECONDS] = self.note_time
        else:
            data[self.OpsNoteFields.OPS_NOTE_HAPPENED_ON_IN_SECONDS] = self.get_ops_note_time(self.note_time)
        return data

    def handle_error_response(self):
        err_msg_template = "Failed to " + str(self.action) + " ops note"
        if not self.info:
            # ops note doesn't exist
            self.fail(err_msg_template + " - Ops note doesn't exist")
        else:
            # err msg received from LM not related to ops note existence
            self.fail(err_msg_template + " \nResponse: " + str(self.info))

    def get_basic_info(self):
        return {self.ModuleFields.ID: self.info.get(self.ModuleFields.ID),
                self.ModuleFields.NOTE: self.info.get(self.ModuleFields.NOTE)}

    def get_basic_info_from_response(self, response):
        return {self.ModuleFields.ID: response.get(self.ModuleFields.ID),
                self.ModuleFields.NOTE: response.get(self.ModuleFields.NOTE)}


def main():
    module = OpsNote()
    module.run()


if __name__ == "__main__":
    main()

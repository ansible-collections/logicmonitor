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
module: lm_otel_collector

short_description: LogicMonitor Otel Collector Ansible module for managing lm otel collectors

version_added: "1.2.0"

author:
    - Anubhav  Singh (@arthuragnar)

description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages collectors within your LogicMonitor account (i.e. add, remove).

extends_documentation_fragment:
    - logicmonitor.integration.lm_auth_options

requirements:
    - Python 'requests' package
    - An existing LogicMonitor account with APM enabled
    - Linux machine

options:
    action:
        description:
            - The action you wish to perform on the otel collector.
            - Add = Install existing otel collector on a Linux machine or add a new otel collector to your LogicMonitor account
              & install it.
            - Remove = Remove a collector from your LogicMonitor account & uninstall it from Linux machine.
        required: true
        type: str
        choices: ['add', 'remove']

    description:
        description:
            - Name of the lmotel collector
        default: 'ansible_otel'
        type: str

    id:
        description:
            - ID of the otel collector.
            - Optional for action=add (only used when installing an existing otel collector).
        type: int
    install_path:
        description:
            - The full path of the directory where the otel collector  should be installed or is installed.
            - Optional for action=add & action=remove
        type: str
        default: '/usr/local/logicmonitor'
    version:
        description:
            - The version of the otel collector to download & install. By default latest otel collector will be installed.
            - Optional for action=add
        type: str
    platform:
        description:
            - The operating system of the platform where playbook will be executed.
            - This field is only relevant for testing purposes.
            - This field should not be provided when using product since collector installation is only supported on
              Linux machines.
        type: str
        default: 'linux'

'''

EXAMPLES = r'''
# Example of adding a collector
- name: Add Collector
  hosts: localhost
  environment:
    OPTS_SILENT: "true"
  become: yes
  tasks:
    - name: Add LogicMonitor collector
      lm_otel_collector:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        install_path: "/usr/local/logicmonitor" #optional
        version: 1.0.0.6

# Example of removing a collector
- name: Remove Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Remove LogicMonitor collector
      lm_otel_collector:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        install_path: "/usr/local/logicmonitor"

'''

RETURN = r'''
---
success:
    description: flag indicating that execution was successful
    returned: success
    type: bool
    sample: True
'''

import os
import platform
import shutil
import subprocess
import signal

# 3rd party imports
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.logicmonitor.integration.plugins.module_utils.logicmonitor_common import \
    LogicMonitorBaseModule

ID = "id"
DESCRIPTION = "description"
COLLECTOR_ID = "collectorId"


class LmotelCollector(LogicMonitorBaseModule):

    def __init__(self):
        """ Initialize the the LogicMonitor Otel Collector object """

        actions = [
            self.ADD,
            self.REMOVE,
        ]

        module_args = dict(
            action=dict(required=True, choices=actions),
            company=dict(required=True),
            access_id=dict(required=True),
            access_key=dict(required=True, no_log=True),
            id=dict(required=False, type="int"),
            description=dict(required=False, default="ansible_otel"),
            install_path=dict(required=False, default="/usr/local/logicmonitor"),
            platform=dict(required=False, default="linux"),
            version=dict(required=False)
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        LogicMonitorBaseModule.__init__(self, module)
        self.module.debug("Instantiating lmotel Collector object")

        self.id = self.params[self.ModuleFields.ID]
        self.description = self.params[self.ModuleFields.DESCRIPTION]

        # self.install_path = self.process_field(self.params[self.ModuleFields.INSTALL_PATH], "/usr/local/logicmonitor")
        # the platform is temporary in order to test downloading in mac machines
        # customers will only be able to install collectors in Linux machines
        self.platform = platform.system().lower()
        if self.platform != "linux":
            self.platform = self.process_field(self.params[self.ModuleFields.PLATFORM]).lower()
        self.version = self.params[self.ModuleFields.VERSION]
        if self.version is not None:
            self.version = self.version.strip().replace(".", "")

        if not HAS_REQUESTS:
            self.fail(
                "This module requires the python 'requests' package."
                "Try `pip install requests` if using Python 2 or `pip3 install requests` if using Python 3.")

    def run(self):
        """ Run module to perform action requested by the user """
        self.module.debug("Running lmotel module...")
        action = self.module.params[self.ModuleFields.ACTION]
        if action == self.ADD:
            self.add()
        elif action == self.REMOVE:
            self.remove()
        else:
            errmsg = ("Unexpected action \"" + str(
                self.module.params[self.ModuleFields.ACTION]) + "\" was specified.")
            self.fail(errmsg)

        self.exit()

    def delete_lmotel_folder(self):
        self.module.debug("Running LmotelCollector.delete_lmotel_folder...")
        bin_dir = os.path.join(self.module.params[self.ModuleFields.INSTALL_PATH], "logicmonitor")
        bin_path = os.path.join(bin_dir, "lmotel", "lmotel")
        if os.path.exists(bin_path):
            try:
                shutil.rmtree(bin_dir)
                self.change = True
                self.module.debug("\ndeleted logicmonitor/lmotel directory")
            except Exception as e:
                self.fail("\nerror deleting logicmonitor folder \n" + str(e))
        else:
            self.module.debug("\nlogicmonitor/lmotel directory does not exists")

    def add(self):
        """ Add LogicMonitor otel collector """
        self.module.debug("Running LmotelCollector.add...")
        # delete logicmonitor/lmotel folder if already exists
        self.delete_lmotel_folder()
        register = self.register_otel_collector()
        try:
            # create a collector on lm account
            lm_otel_id = register['data']['allIds'][0]['id']
        except Exception as e:
            self.fail("Error: LogicMonitor Otel Collector registeration fail.\n" + str(e))
        if lm_otel_id:
            collector_url = register['data']['byId']['lmotelCollectors'][lm_otel_id]['downloadUrl']
            local_filename = "LogicmonitorOtelSetup_" + lm_otel_id + ".bin"
            file = self.download_file(collector_url, local_filename)
            cmd = "chmod +x " + file
            ret_code, out, err = self.module.run_command(cmd)
            if ret_code != 0:
                self.fail(msg="Error: Unable to install collector: " + str(err))
            else:
                self.change = True
                self.module.debug("Collector downloaded successfully")
            # create options file for passing as arguments to the lmotel installer
            if os.path.exists(".lmotel_option.txt"):
                try:
                    os.remove(".lmotel_option.txt")
                    self.change = True
                except Exception as e:
                    self.fail(msg="Error: unable to delete .lmotel_otption.txt file: " + str(e))
            try:
                with open(".lmotel_option.txt", "a+") as f:
                    f.write("y\n" + self.module.params[self.ModuleFields.INSTALL_PATH])
                    f.close()
                    self.change = True
            except Exception as e:
                self.fail(msg="Error: unable to create .lmotel_otption.txt file: " + str(e))

            # setsid is used to run the process in new session, to avoid
            # killing of lmotel process as soon as ansible exits
            cmd = "setsid " + "./" + file + " < .lmotel_option.txt"
            ret_code, out, err = self.module.run_command(cmd)
            # self.module.debug("return code of lmotel bin: " + str(ret_code)+"\n" +str(out) + "\n" + str(err))
            if ret_code != 0:
                self.fail(msg="Error: Unable to install collector: " + str(err))
            else:
                self.module.debug("Collector installed successfully")
                self.change = True

    def download_file(self, url, local_filename):
        self.module.debug("Running LmotelCollector.download_file...")
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        self.change = True
        return local_filename

    def register_otel_collector(self):
        """ Add a collector to a LogicMonitor account """
        self.module.debug("Running LmotelCollector.register_otel_collector...")

        if self.platform != "linux":
            self.fail("Error: LogicMonitor Otel Collector must be installed on a Linux machine.")
        lmotel_url = "/setting/collectors/collector"

        payload = {
            "collectorType": "lmotel",
            "description": self.description,
            "platform": self.platform,
            "version": self.version,
            "enableLMLogs": "false",
        }

        err_msg = "Failed to download lmotel collector installer file from LogicMonitor"
        # generate lmv1 token
        # get downloadurl
        # downloadand install collector
        return self.rest_request(self.POST, data=payload, resource_path=lmotel_url, err_msg=err_msg, collecter_type="lmotel")

    # kill the lmotel process
    # remove otel collector from machine
    def remove(self):
        self.module.debug("Running LmotelCollector.remove...")
        self.kill_process()
        self.delete_lmotel_folder()
        return

    def kill_process(self):
        self.module.debug("Running LmotelCollector.kill_process...")
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.decode().splitlines():
            if 'lmotel' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
                self.module.debug("killed lmotel process with pid:" + str(pid))
                self.change = True


def main():
    module = LmotelCollector()
    module.run()


if __name__ == "__main__":
    main()

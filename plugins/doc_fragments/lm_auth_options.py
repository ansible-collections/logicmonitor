# Copyright 2026 LogicMonitor, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
    options:
        company:
            description:
                - The LogicMonitor account company name.
                - A user logging into their account at "batman.logicmonitor.com" would use "batman".
            required: true
            type: str
        domain:
            description:
                - The LogicMonitor domain name associated with the account.
                - A user logging into "batman.lmgov.us" would use "lmgov.us" as the domain.
                - Defaults to "logicmonitor.com" if not specified.
            required: false
            type: str
            default: logicmonitor.com
        access_id:
            description:
                - The Access ID API token associated with the user's account that's used to query the LogicMonitor API.
                - Please contact your LogicMonitor admin if you need new API tokens created for your account.
            required: true
            type: str
        access_key:
            description:
                - The Access Key API token associated with the user's account that's used to query the LogicMonitor API.
                - Please contact your LogicMonitor admin if you need new API tokens created for your account.
                - Must start with the "!unsafe" keyword if the the key starts with a special character (e.g. '[', ']', etc.)
                  to prevent playbook issues.
            required: true
            type: str
'''

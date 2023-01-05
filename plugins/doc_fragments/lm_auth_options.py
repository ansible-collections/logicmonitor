# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

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

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
        start_time:
            description:
                - The time that the Scheduled Down Time (SDT) should begin.
                - Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm".
                  The former is used for a 24-hr clock while the latter is for a 12-hr clock.
                - Optional for action=sdt.
                - Defaults to the time action is executed.
                - Required in case start time differ from the execution time of action.
            type: str
        end_time:
            description:
                - The time that the Scheduled Down Time (SDT) should end.
                - Format must be 'yyyy-MM-dd HH:mm' or "yyyy-MM-dd HH:mm z" where z is "am" or "pm".
                  The former is used for a 24-hr clock while the latter is for a 12-hr clock.
                - If end time is provided it will be used otherwise duration would be used
                  (duration defaults to 30 min).
                - Optional for action=sdt.
            type: str
        duration:
            description:
                - The duration (minutes) of the Scheduled Down Time (SDT).
                - Optional for action=sdt.
            type: int
            default: 30
        comment:
            description:
                - The note/comment to add to an SDT action.
                - Optional for action=sdt.
            type: str
'''

# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

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

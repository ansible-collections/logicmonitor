=============================================
LogicMonitor Ansible Collection Release Notes
=============================================

.. contents:: Topics

v1.1.4
======

Bug Fixes
-----------

- Fix ignore file permissions

v1.1.3
======

Bug Fixes
-----------

- Fix playbook ``properties`` field array value type JSON deserialization for modifying collector/device/group custom properties that have multiple values.

Feature Enhancement
-------------------

- lm_info: Add ``size`` field to allow users to query more than the default 50 resources (new default value is 250 & max size is 1000).
- Modify resource updating processes to use PATCH rather than UPDATE request method.

v1.1.2
======

Bug Fixes
-----------

- Properly encode HTTP Request parameters

v1.1.1
======

Bug Fixes
-----------

- README: Fixed module links

v1.1.0
======

New Modules
-----------

- lm_collector_group: Manage LogicMonitor collector groups (i.e. add, update, remove)

Feature Enhancement
-------------------

- lm_collector: Add ability to update update collector
- lm_device: Support configuration of Auto-Balanced Collector Groups (ABCG)

v1.0.0
======
- Initial release

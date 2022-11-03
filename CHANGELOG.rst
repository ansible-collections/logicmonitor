=============================================
LogicMonitor Ansible Collection Release Notes
=============================================

.. contents:: Topics

v1.2.1
======

Feature Enhancement
-------------------

- lm_device: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``.
- lm_collector: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``.
- lm_device_group: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``
- lm_collector_group: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``
- lm_datasource: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``
- lm_alert_rule: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``
- lm_escalation_chain: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``
- lm_website_check: Return value now contains ``data`` (resource information), ``action_performed``, ``addition_info``

v1.2.0
======

New Modules
-----------

- lm_alert_rule: Manage LogicMonitor alert rules (i.e. add, update, remove)
- lm_escalation_chain: Manage LogicMonitor escalation chains (i.e. add, update, remove)
- lm_website_check: Manage LogicMonitor website checks (i.e. sdt a ping or web check)
- lm_otel_collector: Manage LogicMonitor otel collectors (i.e. add, remove)

Feature Enhancement
-------------------

- lm_device: Add ``optype`` field to allow user to perform different operation on custom properties while updating.
- lm_collector: Add ``optype`` field to allow user to perform different operation on custom properties while updating.
- lm_device_group: Add ``optype`` field to allow user to perform different operation on custom properties while updating.
- lm_collector_group: Add ``optype`` field to allow user to perform different operation on custom properties while updating.


v1.1.6
======

Bug Fixes
-----------

- Fix update action overwriting custom properties.

v1.1.5
======

Bug Fixes
-----------

- Fix collector installation to accurately use path params ``version`` & ``size``.

Feature Enhancement
-------------------

- lm_collector: Add ``id`` & ``description`` field to allow users to install an existing collector in action=add via its id or description.

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
# LogicMonitor Ansible Collection

[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)

This repository hosts the [LogicMonitor](https://logicmonitor.com) Ansible Collection of LogicMonitor's Ansible
Integration.

LogicMonitor is a hosted, full-stack, infrastructure monitoring platform. This collection includes the Ansible modules
and plugins for interacting with LogicMonitor.

## Requirements

- Ansible version **>=2.10**
- Python **>= 2.7**
- Python [``requests``](https://github.com/psf/requests) module **>=2.24.0**
- An existing LogicMonitor account
- [API tokens](https://logicmonitor.com/support/settings/users-and-roles/api-tokens) for authentication purposes

## Installation

### Installing the Collection from Ansible Galaxy

You can install the LogicMonitor collection with the `ansible-galaxy` CLI:

```bash
ansible-galaxy collection install logicmonitor.integration
```

You can also include it in a `requirements.yml` file and install it
via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
collections:
  - name: logicmonitor.integration
```

### Required Python Libraries

This collection depends upon following third party libraries:

* [`requests`](https://github.com/psf/requests) **>= 2.24.0**

This python module dependencies are not installed by `ansible-galaxy`. It can be manually installed using pip:

```bash
pip install requests
```

or:

```bash
pip install -r requirements.txt
```

## Usage

### Playbooks

To use a module from the LogicMonitor collection, please reference the full namespace, collection name, and module name
that you want to use:

```yaml
---
- name: Using LogicMonitor Collection
  hosts: localhost
  tasks:
    - logicmonitor.integration.lm_collector:
        action: sdt
        company: lm
        access_id: "id123"
        access_key: "key123"
        description: localhost
```

Or you can add the full namespace and collection name in the `collections` element:

```yaml
---
- name: Using LogicMonitor Collection
  hosts: localhost
  collections:
    - logicmonitor.integration
  tasks:
    - lm_collector:
        action: sdt
        company: lm
        access_id: "id123"
        access_key: "key123"
        description: localhost
```

## Included content

### Modules

Name | Description
--- | ---
[logicmonitor.integration.lm_info](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_info_module.md)|Gather information about LogicMonitor objects (i.e. collectors, collector groups, devices, device groups)
[logicmonitor.integration.lm_collector](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_collector_module.md)|Manage LogicMonitor collectors (i.e. add, update, remove, sdt)
[logicmonitor.integration.lm_collector_group](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_collector_group_module.md)|Manage LogicMonitor collector groups (i.e. add, update, remove)
[logicmonitor.integration.lm_otel_collector](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_otel_collector_module.md)|Manage LogicMonitor otel collectors (i.e. add, remove)
[logicmonitor.integration.lm_device](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_device_module.md)|Manage LogicMonitor devices (i.e. add, update, remove, sdt)
[logicmonitor.integration.lm_device_group](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_device_group_module.md)|Manage LogicMonitor device groups (i.e. add, update, remove, sdt)
[logicmonitor.integration.lm_alert_rule](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_alert_rule_module.md)|Manage LogicMonitor alert rules (i.e. add, update, remove)
[logicmonitor.integration.lm_escalation_chain](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_escalation_chain_module.md)|Manage LogicMonitor escalation chains (i.e. add, update, remove)
[logicmonitor.integration.lm_datasource](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_datasource_module.md)|Manage LogicMonitor device datasources (i.e. sdt)
[logicmonitor.integration.lm_website_check](https://github.com/ansible-collections/logicmonitor/blob/main/docs/logicmonitor.integration.lm_website_check_module.md)|Manage LogicMonitor website checks (i.e. sdt a ping or web check)

## Contributing

You can participate in this project
by [submitting bugs and feature requests](https://support.logicmonitor.com/hc/en-us/requests/new), and helping us verify
as they are checked in.

## Release Notes

See the [changelog](https://github.com/ansible-collections/logicmonitor/blob/main/CHANGELOG.rst)

## More information

- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

 BSD (3-clause) License

See [LICENSE](https://github.com/ansible-collections/logicmonitor/blob/main/LICENSE) to see the full text.
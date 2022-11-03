# logicmonitor.integration.lm_alert_rule

Manage LogicMonitor alert rules

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor alert rule (i.e. add, update, remove).

<a name="requirements"></a>

## Requirements

- Python **>= 2.7**
- Python [``requests``](https://github.com/psf/requests) library **>=2.24.0**
- An existing LogicMonitor account
- [API tokens](https://logicmonitor.com/support/settings/users-and-roles/api-tokens) used for authentication. Please
  contact your LogicMonitor admin if you need new API tokens created for your account.

<a name="parameters"></a>

## Parameters

<table  border=0 cellpadding=0 class="documentation-table">
  <tr>
    <th colspan="1">Parameter</th>
    <th>Choices/<font color="blue">Default</font></th>
    <th width="100%">Comments</th>
  </tr>
  <tr>
    <td colspan="1">
      <b>action</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>add</li>
        <li>update</li>
        <li>remove</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The action you wish to perform on the alert rule.</li>
        <li><b>Add:</b> Add an alert rule to your LogicMonitor account.</li>
        <li><b>Update:</b> Update an alert rule in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove an alert rule from your LogicMonitor account.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>company</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The LogicMonitor account company name.</li>
        <li>A user logging into their account at "batman.logicmonitor.com" would use "batman".</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>access_id</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The Access ID API token associated with the user's account that's used to query the LogicMonitor API.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>access_key</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The Access Key API token associated with the user's account that's used to query the LogicMonitor API.</li>
        <li>Must start with the "!unsafe" keyword if the the key starts with a special character (e.g. "[", "]", etc.) to prevent playbook issues.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the alert rule.</li>
        <li>Required for update, remove if name isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The name of the alert rule.</li>
        <li>Required for action=add.</li>
        <li>Required for update, remove id isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>priority</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>A numeric value determining the priority of alert rule.</li>
        <li>"1" represents the highest priority.</li>
        <li>Required for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>level</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>All</li>
        <li>Warn</li>
        <li>Error</li>
        <li>Critical</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Alert severity level to which the alert rule would apply.</li>
        <li>Defaults to "All" when creating rule.</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>datasource</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The datasource for which the alert rule would be applicable.</li>
        <li>Defaults to all datasource when creating rule.</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>datapoint</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The datapoint for which the alert rule would be applicable.</li>
        <li>Defaults to all datapoint when creating rule.</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>instance</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The instance for which the alert rule would be applicable.</li>
        <li>Defaults to all instance when creating rule.</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>groups</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>A comma-separated list of device groups for which the rule would be applicable.</li>
        <li>Defaults to all groups when creating rule.</li>
        <li>Must be enclosed within [] brackets.</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>devices</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>A comma-separated list of devices for which the rule would be applicable.</li>
        <li>Defaults to all devices when creating rule.</li>
        <li>Must be enclosed within [] brackets.</li>
        <li>Optional for managing alert rules (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>suppress_clear</b>
      <div>
        <span>bool</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>True</li>
        <li>False</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>A boolean flag to enable/disable notification of alert clear.</li>
        <li>Defaults to False when creating a rule.</li>
        <li>Optional for managing rules (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>suppress_ACK_STD</b>
      <div>
        <span>bool</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>True</li>
        <li>False</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>A boolean flag to enable/disable notification of alert SDT and Acknowledge.</li>
        <li>Defaults to False when creating a rule.</li>
        <li>Optional for managing rules (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>escalation_chain_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>ID of escalation chain to which the alert would be sent.</li>
        <li>Required for action=add.</li>
        <li>Optional for managing rules action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>escalation_interval</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>the amount of time(min) that should elapse before an alert will be escalated to the next stage.</li>
        <li>Required for action=add.</li>
        <li>Optional for managing rules action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>resource_properties_filter</b>
      <div>
        <span>dictionary</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>A JSON object of properties that a resource or website must possess in order for this alert rule to match.</li>
        <li>A maximum of five property filters can be specified.</li>
        <li>Multiple property filters are joined by an AND logical operator.</li>
        <li>Must be enclosed within {} braces.</li>
        <li>Optional for managing rules (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>force_manage</b>
      <div>
        <span>boolean</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>True</li>
        <li>False</li>
      </ul>
      <b>Default:</b>
      <ul>
        <li>True</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>A boolean flag to enable/disable the feature to <br>(1) update an alert rule when the initial action=add because the rule exists <br>or<br> (2) add an alert rule when the initial action=update because the rule doesn't exist</li>
        <li>Optional for managing alert rule (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Alert Rule
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Alert Rule
      lm_alert_rule:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: Ansible-Rule
        priority: 55
        level: All
        suppress_clear: false
        suppress_ACK_STD: false
        escalation_chain_id: 2
        escalation_interval: 25

---
- name: Update Alert Rule
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Alert Rule
      lm_alert_rule:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: Ansible-Rule
        id: 16
        priority: 55
        level: All
        datasource: Ping
        datapoint: Ping
        instance: Ping
        groups: ["Customer", "Devices by Type"]
        devices: ["192.168.147.131", "127.0.0.1_collector_2"]
        suppress_clear: true
        suppress_ACK_STD: true
        escalation_chain_id: 2
        escalation_interval: 25
        resource_properties_filter : {"key1": "value1","key2": "value2"}

---
- name: Remove Alert Rule
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Alert Rule
      lm_alert_rule:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: Ansible-Rule
        id: 16
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
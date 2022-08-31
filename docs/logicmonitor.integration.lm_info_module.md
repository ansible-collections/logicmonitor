# logicmonitor.integration.lm_info

Gather information about LogicMonitor objects (i.e. collectors, devices, device groups, etc).

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to gather information about LogicMonitor objects (i.e. collectors, collector groups, devices,
  device groups, etc).

<a name="requirements"></a>

## Requirements

- Python **>= 2.7**
- Python [``requests``](https://github.com/psf/requests) library **>=2.24.0**
- An existing LogicMonitor account
- [API tokens](https://logicmonitor.com/support/settings/users-and-roles/api-tokens) used for    
  authentication. Please contact your LogicMonitor admin if you need new API tokens created for your account.

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
      <b>target</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>collector</li>
        <li>collector_group</li>
        <li>device</li>
        <li>device_group</li>
        <li>alert_rule</li>
        <li>escalation_chain</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The type of LogicMonitor object you wish to query.</li>
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
        <li>The ID of the collector, device, device group, alert rule, etc to target.</li>
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
        <li>The name of the collector group, alert rule, escalation chain, etc to target.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>description</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The description of the collector to target.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>display_name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The display name of the device to target.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>hostname</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The name (hostname) of the device to target.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>full_path</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The full path of the device group to target.</li>
        <li>The Root group full_path should be denoted by empty string "" or "/".</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>size</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The number of resources/results to display (default is 250 & max is 1000)</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Gather information about all collectors
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about a collector
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about all collector groups
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector_group
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about a collector group
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: collector_group
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: "collector group"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about all devices
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about a device
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device
        company: batman
        access_id: "id123"
        access_key: "key123"
        hostname: "127.0.0.1"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about all device groups
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device_group
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about a device group
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: device_group
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

---
- name: Gather information about all alert rules
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: alert_rule
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'
        
---        
- name: Gather information about a alert rule
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: alert_rule
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'
---        
- name: Gather information about all escalation chains
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: escalation_chain
        company: batman
        access_id: "id123"
        access_key: "key123"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'
---        
- name: Gather information about an escalation chain
  hosts: localhost
  tasks:
    - name: Running module
      lm_info:
        target: escalation_chain
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 16
      register: output
    - name: Output
      debug:
        msg: '{{ output }}'

```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
, the following are the fields unique to this module:

<table  border=0 cellpadding=0 class="documentation-table">
  <tr>
    <th colspan="1">Key</th>
    <th>Returned</th>
    <th width="100%">Description</th>
  </tr>
  <tr>
    <td colspan="1">
      <b>data</b>
      <div>
        <span>dictionary</span>
      </div>
    </td>
    <td>success</td>
    <td>Dictionary containing list of collectors/devices/groups or a single JSON object containing information of a specific collector/device/group</td>
  </tr>
</table>

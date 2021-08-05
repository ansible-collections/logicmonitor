# logicmonitor.integration.lm_device

Manage LogicMonitor devices

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor devices (i.e. add, update, remove, SDT).

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
        <li>sdt</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The action you wish to perform on the device.</li>
        <li><b>Add:</b> Add a device to your LogicMonitor account.</li>
        <li><b>Update:</b> Update a device in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove a device from your LogicMonitor account.</li>
        <li><b>SDT:</b> Schedule downtime for a device in your LogicMonitor account.</li>
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
        <li>The ID of the device.</li>
        <li>Required for update, remove, sdt if both display_name and hostname aren't provided.</li>
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
        <li>The display name of the device.</li>
        <li>Required for action=add.</li>
        <li>Required for update, remove, sdt if both id and hostname aren't provided.</li>
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
        <li>The hostname (name) of the device.</li>
        <li>Required for action=add.</li>
        <li>Required for update, remove, sdt if both id and display_name aren't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>auto_balance</b>
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
    </td>
    <td>
      <ul>
        <li>A boolean flag to denote whether or not the collector group configured for the device should use auto balancing.</li>
        <li>This value should only be True when the configured collector group is an Auto-Balanced Collector Group (ABCG).</li>
        <li>Optional for managing devices (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>collector_group_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the collector group to configure for the device.</li>
        <li>Required for action=add if an ABCG is being configured (auto_balance=True) and collector_group_name isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>collector_group_name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The name of the collector group to configure for the device.</li>
        <li>The default/Ungrouped group name should be denoted by empty string "" or "@default".</li>
        <li>Required for action=add if an ABCG is being configured (auto_balance=True) and collector_group_name isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>collector_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the collector to monitor the newly added device.</li>
        <li>Required for action=add if a non-ABCG is being configured (auto_balance=False) and collector_description isn't provided.</li>
        <li>NOTE: A collector can't be manually configured for an existing device (action=update) when an ABCG is in use and auto balance isn't being disabled.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>collector_description</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The description of the collector to monitor the newly added device.</li>
        <li>Required for action=add if a non-ABCG is being configured (auto_balance=False) and collector_id isn't provided.</li>
        <li>NOTE: A collector can't be manually configured for an existing device (action=update) when an ABCG is in use and auto balance isn't being disabled.</li>
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
        <li>A comma-separated list of device groups that the device should be a member of.</li>
        <li>The list can contain device group IDs and/or full paths.</li>
        <li>Must be enclosed within [] brackets.</li>
        <li>Optional for managing devices (action=add or action=update).</li>
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
        <li>The long text description of the device to add.</li>
        <li>Optional for managing devices (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>disable_alerting</b>
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
    </td>
    <td>
      <ul>
        <li>A boolean flag to enable/disable alerting for a device.</li>
        <li>Defaults to False when creating a device.</li>
        <li>Must be enclosed within {} braces.</li>
        <li>Optional for managing devices (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>properties</b>
      <div>
        <span>dictionary</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>A JSON object of properties to configure for the LogicMonitor device.</li>
        <li>This parameter will add or update existing properties in your LogicMonitor account.</li>
        <li>Optional for managing devices (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>start_time</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The time that the Scheduled Down Time (SDT) should begin.</li>
        <li>Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm". 
              The former is used for 24-hr clock while the latter is a 12-hr clock.</li>
        <li>Optional for action=sdt.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>end_time</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The time that the Scheduled Down Time (SDT) should end.</li>
        <li>Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm". 
              The former is used for a 24-hr clock while the latter is for a 12-hr clock.</li>
        <li>Optional for action=sdt.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>duration</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
      <b>Default:</b>
      <ul>
        <li>30</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The duration (minutes) of the Scheduled Down Time (SDT).</li>
        <li>Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm". 
              The former is used for a 24-hr clock while the latter is for a 12-hr clock.</li>
        <li>Optional for action=sdt.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>comment</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The note/comment to add to an SDT action.</li>
        <li>Optional for action=sdt.</li>
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
        <li>A boolean flag to enable/disable the feature to <br>(1) update a device when the initial action=add because the device exists <br>or<br> (2) add a device when the initial action=update because the device doesn't exist</li>
        <li>Optional for managing devices (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Device
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Device
      lm_device:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "Ansible Device"
        hostname: 127.0.0.1
        collector_id: 1
        groups: [ "Devices by Type/Misc", 4 ]
        description: "test"
        disable_alerting: true
        properties: {
          snmp.community: commstring,
          type: dev
        }

---
- name: Update Device
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Device
      lm_device:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1
        display_name: "New Ansible Device"
        hostname: 127.0.0.1
        collector_description: "localhost 123"
        groups: [ "Devices by Type/Misc", 4 ]
        description: "test"
        disable_alerting: true
        properties: {
          snmp.community: commstring,
          type: dev
        }

---
- name: Remove Device
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Device
      lm_device:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "Ansible_Device"

---
- name: SDT Device
  hosts: localhost
  tasks:
    - name: Place LogicMonitor device into Scheduled downtime (default is 30 min.)
      logicmonitor:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        display_name: "127.0.0.1_collector_4"
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
# logicmonitor.integration.lm_collector

Manage LogicMonitor collectors

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor collectors (i.e. add, remove, SDT).

<a name="requirements"></a>

## Requirements

- Python **>= 2.7**
- Python [``requests``](https://github.com/psf/requests) library **>=2.24.0**
- An existing LogicMonitor account
- [API tokens](https://logicmonitor.com/support/settings/users-and-roles/api-tokens) used for authentication. Please
  contact your LogicMonitor admin if you need new API tokens created for your account.
- Linux machine when adding/installing/removing a collector

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
        <li>The action you wish to perform on the collector.</li>
        <li><b>Add:</b> Add a collector to your LogicMonitor account & install it on Linux machine.</li>
        <li><b>Update:</b> Update a collector in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove a collector from your LogicMonitor account & uninstall it from Linux machine.</li>
        <li><b>SDT:</b> Schedule downtime for a collector in your LogicMonitor account.</li>
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
        <li>The ID of the collector.</li>
        <li>Required for update, remove, sdt if description isn't provided.</li>
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
        <li>The description of the collector.</li>
        <li>Optional for action=add.</li>
        <li>Required for update, remove, sdt if id isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>install_path</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Default:</b>
      <ul>
        <li>/usr/local/logicmonitor</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The full path of the directory where the collector agent should be installed or is installed.</li>
        <li>Optional for action=add & action=remove.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>install_user</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Default:</b>
      <ul>
        <li>logicmonitor</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The username to associate with the installed collector.</li>
        <li>Optional for action=add.</li>
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
        <li>The ID of the collector group associated with the collector being added.</li>
        <li>Optional for action=add.</li>
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
        <li>The name of the collector group associated with the collector being added.</li>
        <li>The default/Ungrouped collector group should be denoted by empty string "" or "@default".</li>
        <li>Optional for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>device_group_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the device group associated with the collector being added.</li>
        <li>Optional for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>device_group_full_path</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The full path of the device group associated with the collector being added.</li>
        <li>The default/root device group should be denoted by empty string "" or "/".</li>
        <li>Optional for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>version</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The version of the collector to download & install.</li>
        <li>General release (version 29.003) is typically recommended.</li>
        <li>Defaults to the latest GD Collector.</li>
        <li>Optional for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>size</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>nano (<2GB>)</li>
        <li>small (2GB)</li>
        <li>medium (4GB)</li>
        <li>large (8GB)</li>
      </ul>
      <b>Default:</b>
      <ul>
        <li>small</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The size of the collector to download & install.</li>
        <li>Optional for action=add.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>escalating_chain_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the escalation chain to configure for the collector being updated.</li>
        <li>0 denotes to not assign any escalation chain (i.e. disable alert routing/notifications)</li>
        <li>Optional for action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>escalating_chain_name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The name of the escalation chain to configure for the collector being updated.</li>
        <li>Optional for action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>backup_collector_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the failover collector to configure for the collector being updated.</li>
        <li>0 denotes to not assign any failover collector.</li>
        <li>Optional for action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>backup_collector_description</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The long text description of the failover collector to configure for the collector being updated.</li>
        <li>Optional for action=update.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>resend_collector_down_alert_interval</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The interval, in minutes, after which collector down alert notifications will be resent.</li>
        <li>0 denotes to send the collector down alert once.</li>
        <li>Optional for action=update.</li>
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
        <li>A JSON object of properties to configure for the LogicMonitor collector.</li>
        <li>This parameter will add or update existing properties in your LogicMonitor account.</li>
        <li>Optional for action=update.</li>
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
        <li>A boolean flag to enable/disable the feature to add a collector when the initial action=update because the collector doesn't exist.</li>
        <li>Optional for action=update.</li>
      </ul>
    </td>
  </tr>

</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Add LogicMonitor collector
      lm_collector:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        collector_group_name: "test group"
        device_group_full_path: "Devices by Type/Test Group"
        platform: "Linux"
        version: "29.107"
        size: "large"

---
- name: Update Collector
  hosts: localhost
  tasks:
    - lm_collector:
        action: Update LogicMonitor collector
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1
        description: "localhost new"
        escalating_chain_name: "ansible chain"
        backup_collector_id: 1
        resend_collector_down_alert_interval: 60
        properties: {
          "size": "medium"
        }

---
- name: Remove Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Remove LogicMonitor collector
      lm_collector:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 1

---
- name: SDT Collector
  hosts: localhost
  tasks:
    - name: Place LogicMonitor collector into Scheduled downtime (default is 30 min.)
      lm_collector:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        start_time: "1/1/2022 15:00"
        duration: 60
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.

# logicmonitor.integration.lm_device_group

Manage LogicMonitor device groups

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor device groups (i.e. add, update, remove, SDT).

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
        <li>The action you wish to perform on the device group.</li>
        <li><b>Add:</b> Add a device group to your LogicMonitor account.</li>
        <li><b>Update:</b> Update a device group in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove a device group from your LogicMonitor account.</li>
        <li><b>SDT:</b> Schedule downtime for a device group in your LogicMonitor account.</li>
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
        <li>The ID of the device group.</li>
        <li>Required for update, remove, sdt if full_path isn't provided.</li>
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
        <li>Required for action=add.</li>
        <li>Required for update, remove, sdt if id isn't provided.</li>
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
        <li>The ID of the collector to monitor newly the added device group.</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
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
        <li>The description of the collector to monitor the newly added device group.</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
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
        <li>The long text description of the device group to add.</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
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
        <li>A boolean flag to enable/disable alerting for a device group.</li>
        <li>Defaults to False when creating a device.</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
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
        <li>A JSON object of properties to configure for the LogicMonitor device group.</li>
        <li>This parameter will add or update existing properties in your LogicMonitor account.</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>datasource_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The ID of the device group datasource in your LogicMonitor account to SDT.</li>
        <li>If datasource_id & datasource_name are not supplied for device group SDT, all datasources under the group are SDT'd.</li>
        <li>Optional for action=sdt.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>datasource_name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The name of the device group datasource in your LogicMonitor account to SDT.</li>
        <li>If datasource_id & datasource_name are not supplied for device group SDT, all datasources under the group are SDT'd.</li>
        <li>Optional for action=sdt.</li>
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
     <td>
      <b>Default:</b>
      <ul>
        <li>the time action was executed</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The time that the Scheduled Down Time (SDT) should begin.</li>
        <li>Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm". 
              The former is used for 24-hr clock while the latter is a 12-hr clock.</li>
        <li>Optional for action=sdt.</li>
        <li>Defaults to the time action is executed.</li>
        <li>Required in case start time differ from the execution time of action.</li>
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
        <li>If end time is provided it will be used otherwise duration would be used (duration defaults to 30 min)</li>
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
        <li>A boolean flag to enable/disable the feature to <br>(1) update a device group when the initial action=add because the group exists <br>or<br> (2) add a device group when the initial action=update because the group doesn't exist</li>
        <li>Optional for managing device groups (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>optype</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>refresh</li>
        <li>replace</li>
        <li>add</li>
      </ul>
      <b>Default:</b>
      <ul>
        <li>replace</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>A string describing the operation on properties when updating device group </li>
        <li><b>replace</b> - a property would be updated if it exists already else a new property will be created</li>
        <li><b>refresh</b> - a property would be updated if it exists already else a new property will be created,<br> any existing property not provided during update will be removed</li>
        <li><b>add</b> - a property would be ignored if it exists already else a new property will be created</li>
        <li>Optional for managing device groups (action=update).</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Device Group
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Device Group
      lm_device_group:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors/Ansible Group"
        collector_id: 1
        description: "test"
        disable_alerting: true
        properties: {
          snmp.community: commstring,
          type: dev
        }

---
- name: Update Device Group
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Device Group
      lm_device_group:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
        collector_id: 1
        description: "test"
        disable_alerting: true
        properties: {
          snmp.community: commstring,
          type: dev
        }
        optype: add

---
- name: Remove Device Group
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Device Group
      lm_device_group:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: 123

---
- name: SDT Device Group
  hosts: localhost
  tasks:
    - name: Place LogicMonitor device group into Scheduled downtime.
      lm_device_group:
        action: sdt
        company: batman
        access_id: "id123"
        access_key: "key123"
        full_path: "Devices by Type/Collectors"
        datasource_id: 123
        datasource_name: "ping"
        duration: 60
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
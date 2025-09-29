# logicmonitor.integration.lm_datasource

Manage LogicMonitor device datasources

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor device datasources (i.e. SDT).

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
        <li>sdt</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The action you wish to perform on the datasource.</li>
        <li><b>SDT:</b> Schedule downtime for a device datasource in your LogicMonitor account.</li>
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
      <b>domain</b>
      <div>
        <span>string</span>
      </div>
    <td>
      <b>Default:</b>
      <ul>
        <li>logicmonitor.com</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The LogicMonitor domain name associated with the account.</li>
        <li>A user logging into "batman.lmgov.us" would use "lmgov.us" as the domain.</li>
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
        <li>The ID of the device datasource.</li>
        <li>Required for action=sdt if name isn't provided.</li>
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
        <li>Name of the device datasource to target.</li>
        <li>Required for action=sdt if id isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>device_id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>ID of device (containing datasource) to target.</li>
        <li>
          Required for action=sdt if the following are true:<br>
            (1) id of datasource isn't provided<br>
            (2) name of datasource is provided<br>
            (3) device_display_name isn't provided<br>
            (4) device_hostname isn't provided
        </li>
      </ul>
    </td>
  </tr>
    <tr>
    <td colspan="1">
      <b>device_display_name</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The display name of device (containing datasource) to target.</li>
        <li>
          Required for action=sdt if the following are true:<br>
            (1) id of datasource isn't provided<br>
            (2) name of datasource is provided<br>
            (3) device_id isn't provided<br>
            (4) device_hostname isn't provided
        </li>
      </ul>
    </td>
  </tr>
    <tr>
    <td colspan="1">
      <b>device_hostname</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The hostname (name) of device (containing datasource) to target.</li>
        <li>
          Required for action=sdt if the following are true:<br>
            (1) id of datasource isn't provided<br>
            (2) name of datasource is provided<br>
            (3) device_id isn't provided<br>
            (4) device_display_name isn't provided
        </li>
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
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: SDT Datasource
  hosts: localhost
  tasks:
    - name: Place LogicMonitor datasource into Scheduled downtime.
      logicmonitor:
        action: sdt
        company: batman
        domain: lmgov.us
        access_id: "id123"
        access_key: "key123"
        name: "ping"
        device_display_name: "127.0.0.1_collector_1"
        start_time: "1/1/2022 15:00"
        duration: 60
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
# logicmonitor.integration.lm_collector_group

Manage LogicMonitor collector groups

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor collector groups (i.e. add, update, remove).

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
        <li>The action you wish to perform on the collector group.</li>
        <li><b>Add:</b> Add a collector group to your LogicMonitor account.</li>
        <li><b>Update:</b> Update a collector group in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove a collector group from your LogicMonitor account.</li>
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
        <li>The ID of the collector group.</li>
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
        <li>The name of the collector group to target.</li>
        <li>The default group name should be denoted by empty string "" or "@default".</li>
        <li>Required for action=add.</li>
        <li>Required for update, remove if id isn't provided.</li>
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
        <li>The long text description of the collector group to add.</li>
        <li>Optional for managing collector groups (action=add or action=update).</li>
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
        <li>A JSON object of properties to configure for the LogicMonitor collector group.</li>
        <li>This parameter will add or update existing properties in your LogicMonitor account.</li>
        <li>Optional for managing collector groups (action=add or action=update).</li>
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
        <li>A boolean flag to denote whether or not the collector group should be an Auto-Balanced Collector Group (ABCG).</li>
        <li>Optional for managing collector groups (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>instance_threshold</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The instance count threshold for a Collector in an Auto-Balanced Collector Group (ABCG) is auto-calculated using the ABCG's assigned threshold value and the RAM on the Collector machine.</li>
        <li>By default, this threshold is set to 10,000 instances, which represents the instance count threshold for a medium-sized Collector that uses 2 GB of RAM.</li>
        <li>Only values greater than or equal to 0 will be used.</li>
        <li>The number of instances that a Collector can handle is calculated with the following formula:</li>
        <ul>
          <li>Number of instances = (Target_Collector_mem/Medium_mem)^1/2 * Medium_Threshold</li>
        </ul>
        <li>Approximate Instance Thresholds (based on medium-sized Collector threshold limit):</li>
        <table>
          <tr>
            <td>
              <b>small</b>
            </td>
            <td>
              <b>medium</b>
            </td>
            <td>
              <b>large</b>
            </td>
          </tr>
          <tr>
            <td>4950</td>
            <td>7000</td>
            <td>9900</td>
          </tr>
          <tr>
            <td>7070</td>
            <td>10000</td>
            <td>14140</td>
          </tr>
          <tr>
            <td>10600</td>
            <td>15000</td>
            <td>21210</td>
          </tr>
        </table>
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
        <li>A boolean flag to enable/disable the feature to <br>(1) update a collector group when the initial action=add because the group exists <br>or<br> (2) add a collector group when the initial action=update because the group doesn't exist</li>
        <li>Optional for managing collector groups (action=add or action=update).</li>
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
        <li>A string describing the operation on properties when updating collector group </li>
        <li><b>replace</b> - a property would be updated if it exists already else a new property will be created</li>
        <li><b>refresh</b> - a property would be updated if it exists already else a new property will be created,<br> any existing property not provided during update will be removed</li>
        <li><b>add</b> - a property would be ignored if it exists already else a new property will be created</li>
        <li>Optional for managing collector groups (action=update).</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Collector Group
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Collector Group
      lm_collector_group:
        action: add
        company: batman
        domain: lmgov.us
        access_id: "id123"
        access_key: "key123"
        name: "Collector Group"
        description: "test"
        disable_alerting: true
        properties: {
          type: dev
        }

---
- name: Update Collector Group
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Collector Group
      lm_collector_group:
        action: update
        company: batman
        domain: lmgov.us
        access_id: "id123"
        access_key: "key123"
        id: 123
        name: "Collector Group New"
        disable_alerting: false
        properties: {
          type2: dev2
        }
        optype: add

---
- name: Remove Collector Group
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Collector Group
      lm_collector_group:
        action: remove
        company: batman
        domain: lmgov.us
        access_id: "id123"
        access_key: "key123"
        name: "collector group"
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
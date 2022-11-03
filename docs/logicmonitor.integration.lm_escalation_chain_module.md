# logicmonitor.integration.lm_escalation_chain

Manage LogicMonitor escalation chain

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor escalation chain (i.e. add, update, remove).

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
        <li>The action you wish to perform on the escalation chain.</li>
        <li><b>Add:</b> Add an escalation chain to your LogicMonitor account.</li>
        <li><b>Update:</b> Update an escalation chain in your LogicMonitor account.</li>
        <li><b>Remove:</b> Remove an escalation chain from your LogicMonitor account.</li>
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
        <li>The ID of the escalation chain.</li>
        <li>Required for managing escalation chain (action=update and action=remove) if name isn't provided.</li>
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
        <li>The name of the escalation chain.</li>
        <li>Required for managing escalation chain (action=add).</li>
        <li>Required for managing escalation chain (action=update and action=remove) if id isn't provided.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>enable_throttling</b>
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
        <li>A boolean flag to enable/disable alert throttling.</li>
        <li>Required for managing escalation chain (action=add).</li>
        <li>Optional for managing escalation chain (action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>rate_limit_alerts</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>The maximum number of alert notifications that can be delivered during the Rate Limit Period.</li>
        <li>Note that re-sent alert notifications count towards this number.</li>
        <li>Required for managing escalation chain (action=add and action=update) if enable_throttling is set to true.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>rate_limit_period</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>The period (minutes) over which max number of alerts (specified in rate_limit_alerts) can be sent out.</li>
        <li>Required for managing escalation chain (action=add and action=update) if enable_throttling is set to true.</li>
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
    <td>
    </td>
    <td>
      <ul>
        <li>Description of escalation chain.</li>
        <li>Optional for managing escalation chain (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>destinations</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>A comma separated ordered list of stages.</li>
        <li>Stages is a comma separated list of recipients.</li>
        <li>Required for managing escalation chain (action=add).</li>
        <li>Optional for managing escalation chain (action=update).</li>
        <li>Recipient is a JSON object pointing to any one of the following: <br><br>(1) <b>integration</b> - send alerts to integrations (sms, email, pagerduty, autotask, etc...) 
            <br>required properties: <br>name - name of the integration <br>user - logicmonitor username <br>Note: in case of email, sms and voice name would be the type (ie for email name would be email)
            <br><br>(2) <b>arbitrary emails</b> - send alerts to the given email address <br>required properties: <br>name - name must be "arbitrary-email" <br>address - email address
            <br><br>(3) <b>recipient group</b> - send alerts to a recipient group <br>required properties: <br>name - name must be "group" <br>group-name - name of the group
        </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>cc_destinations</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td>
    </td>
    <td>
      <ul>
        <li>cc destination is a list of recipients.</li>
        <li>Recipients in cc will receive all notifications sent to every stage in the escalation chain.</li>
        <li>Optional for managing escalation chain (action=add or action=update).</li>
        <li>Recipient is a JSON object pointing to any one of the following: <br><br>(1) <b>integration</b> - send alerts to integrations (sms, email, pagerduty, autotask, etc...) 
            <br>required properties: <br>name - name of the integration <br>user - logicmonitor username <br>Note: in case of email, sms and voice name would be the type (ie for email name would be email)
            <br><br>(2) <b>arbitrary emails</b> - send alerts to the given email address <br>required properties: <br>name - name must be "arbitrary-email" <br>address - email address
            <br><br>(3) <b>recipient group</b> - send alerts to a recipient group <br>required properties: <br>name - name must be "group" <br>group-name - name of the group
        </li>
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
        <li>A boolean flag to enable/disable the feature to <br>(1) update an escalation chain when the initial action=add because the chain exists <br>or<br> (2) add an escalation chain when the initial action=update because the chain doesn't exist</li>
        <li>Optional for managing escalation chain (action=add or action=update).</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: Add Escalation Chain
  hosts: localhost
  tasks:
    - name: Add LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
        enable_throttling: True
        rate_limit_period: 22
        rate_limit_alerts: 33
        description: added from ansible
        destinations: [
          [
            {"name":"ConnectWise Integration-clone", "user":"john.doe@logicmonitor.com"},
            {"name":"group", "group-name":"test-group"},
            {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"}
          ],
          [
            {"name":"email","user":"john.doe@logicmonitor.com" },
            {"name":"voice","user":"john.doe@logicmonitor.com" }
           ]
        ]
        cc_destinations: [
          {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"},
          {"name":"arbitrary-email", "address":"john.doe@google.com"},
          {"name":"Autotask Integration -New", "user":"john.doe@logicmonitor.com"}
        ]

---
- name: Update Escalation Chain
  hosts: localhost
  tasks:
    - name: Update LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
        enable_throttling: false
        rate_limit_period: 22
        rate_limit_alerts: 33
        description: added from ansible
        destinations: [
          [
            {"name":"ConnectWise Integration-clone", "user":"john.doe@logicmonitor.com"},
            {"name":"group", "group-name":"test-group"},
            {"name":"arbitrary-email", "address":"john.doe@logicmonitor.com"}
          ],
          [
            {"name":"email","user":"john.doe@logicmonitor.com" },
            {"name":"voice","user":"john.doe@logicmonitor.com" }
           ]
        ]
---
- name: Remove Escalation Chain
  hosts: localhost
  tasks:
    - name: Remove LogicMonitor Escalation Chain
      lm_escalation_chain:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        name: new-chain
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.
# logicmonitor.integration.webhook_event_source

Webhook event source to get alerts/events from logicmonitor

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [More information](#more-information)

<a name="synopsis"></a>

## Synopsis

- This event source can be used to automate remediation of alert generated in LogicMonitor.

<a name="requirements"></a>

## Requirements

- Python **>= 2.7**
- Python requirements.txt
- An existing LogicMonitor account
- Ansible Integration with generated ansible_token
- Ansible-vault encrypted file with ansible_token

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
      <b>host</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td>
      <b>Default:</b>
      <ul>
        <li>127.0.0.1</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The hostname to listen to</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>port</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td><b>Default:</b>
      <ul>
        <li>5000</li>
      </ul></td>
    <td>
      <ul>
        <li>The port to listen to</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>vault_pass</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>Password that was used to encrypt the file containing the Ansible Token</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <b>vault_path</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>Path to vault file containing Ansible Token</li>
      </ul>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
---
- name: collector down mitigation
  hosts: localhost
  sources:
    - logicmonitor.integration.webhook:
        hosts: 127.0.0.1
        port: 5000
        vault_pass: '{{vault_pass}}'
        vault_path: '{{vault_path}}'
  rules:
    - name: start collector
      condition: event.payload.type == "agentDownAlert"
      action:
        run_playbook:
          name: logicmonitor.integration.start_lm-collector

---
- name: webhook alert events
  hosts: localhost
  sources:
    - logicmonitor.integration.webhook:
        hosts: 127.0.0.1
        port: 5000
        vault_pass: '{{vault_pass}}'
        vault_path: '{{vault_path}}'
  rules:
    - name: run custom script for alert mitigation
      condition: event.payload.type == "alert"
      action:
        run_playbook:
          name: logicmonitor.integration.run_script
```

<a name="More information"></a>

## More information

- [Ansible Rulebook Introduction](https://ansible.readthedocs.io/projects/rulebook/en/latest/getting_started.html)
- [Event Driven Ansible Introduction](https://www.ansible.com/blog/getting-started-with-event-driven-ansible)


# logicmonitor.integration.lm_otel_collector

Manage LogicMonitor collectors

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor otel collectors (i.e. add, remove).

<a name="requirements"></a>

## Requirements

- Python **>= 2.7**
- Python [``requests``](https://github.com/psf/requests) library **>=2.24.0**
- An existing LogicMonitor account with APM enabled
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
        <li>remove</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>The action you wish to perform on the otel collector.</li>
        <li><b>Add:</b> Add a new lmotel collector to your LogicMonitor account & install it.</li>
        <li><b>Remove:</b> Uninstall a lmotel collector from Linux machine.</li>
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
      <b>description</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The description of the collector.</li>
        <li>Required for action=add.</li>
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
      <b>version</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The version of the collector to download & install.</li>
        <li>Not needed for action=remove, Optional for action=add, if version is not provided , it will pick the latest available version</li>
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
  environment:
    OPTS_SILENT: "true"
  become: yes
  tasks:
    - name: Add LogicMonitor collector
      lm_otel_collector:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        description: "localhost"
        version: "1.0.0.6"

---
- name: Remove Collector
  hosts: localhost
  become: yes
  tasks:
    - name: Remove LogicMonitor collector
      lm_otel_collector:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        install_path: "/usr/local/logicmonitor"
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)
.

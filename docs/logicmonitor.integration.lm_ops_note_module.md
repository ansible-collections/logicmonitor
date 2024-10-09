# logicmonitor.integration.lm_ops_note

Manage LogicMonitor ops notes

- [Synopsis](#synopsis)
- [Requirements](#requirements)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)

<a name="synopsis"></a>

## Synopsis

- This module can be used to manage LogicMonitor ops notes (i.e. add, update, remove).

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
      <a name="action"></a>
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
      <div>The action you want to perform on the ops note.</div>
      <div>Required for all operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="note"></a>
      <b>note</b>
      <div>
        <span>string</span>
      </div>
    </td>
    <td></td>
    <td>
      <div>The content of the ops note.</div>
      <div>Required for add and update operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="id"></a>
      <b>id</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <div>The ID of the ops note.</div>
      <div>Required for update and remove operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="tags"></a>
      <b>tags</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td></td>
    <td>
      <div>The tags associated with the ops note.</div>
      <div>Optional for add and update operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="scopes"></a>
      <b>scopes</b>
      <div>
        <span>list</span>
      </div>
    </td>
    <td></td>
    <td>
      <div>The scopes associated with the ops note. Scopes are IDs of the resources to which the ops note applies.</div>
      <div>Optional for add and update operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="scope_type"></a>
      <b>scope_type</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td>
      <b>Choices:</b>
      <ul>
        <li>device</li>
        <li>device_group</li>
        <li>website</li>
      </ul>
    </td>
    <td>
      <div>The type of scope associated with the ops note.</div>
      <div>Optional for add and update operations.</div>
    </td>
  </tr>
  <tr>
    <td colspan="1">
      <a name="note_time"></a>
      <b>note_time</b>
      <div>
        <span>integer</span>
      </div>
    </td>
    <td></td>
    <td>
      <ul>
        <li>The time that the Ops note should be created.</li>
        <li>Format must be "yyyy-MM-dd HH:mm" or "yyyy-MM-dd HH:mm z" where z is "am" or "pm". 
              The former is used for 24-hr clock while the latter is a 12-hr clock.</li>
        <li>Defaults to the time action is executed.</li>
        <li>Required in case note time differs from the execution time of action.</li>
    </td>
  </tr>
</table>

<a name="examples"></a>

## Examples

```yaml
- name: Add Ops Note
  hosts: localhost
  collections:
    - logicmonitor.integration
  tasks:
    - name: Running module
      lm_ops_note:
        action: add
        company: batman
        access_id: "id123"
        access_key: "key123"
        note: "This is a test ops note"
        tags: [ "MyTag", "MyOtherTag" ]
        scope_type: "device"
        scopes: [ "123", "456" ]
      register: output
    - name: Output
      debug:
        msg: '{{ output }}' 
```

```yaml
- name: Update Ops Note
  hosts: localhost
  collections:
    - logicmonitor.integration
  tasks:
    - name: Running module
      lm_ops_note:
        action: update
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: "cNaa1ByBTOSIBi7V61JmVg"
        note: "This is an updated test ops note"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}' 
```

```yaml
- name: Remove Ops Note
  hosts: localhost
  collections:
    - logicmonitor.integration
  tasks:
    - name: Running module
      lm_ops_note:
        action: remove
        company: batman
        access_id: "id123"
        access_key: "key123"
        id: "cNaa1ByBTOSIBi7V61JmVg"
      register: output
    - name: Output
      debug:
        msg: '{{ output }}' 
```

<a name="return-values"></a>

## Return Values

Common return values are
documented [here](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values)

#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_ports.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_ports

short_description: Manage Meraki switch port configuration

description:
  - Manage per-device switch port configuration for Meraki switches.
  - Device-scoped (uses serial number, not network_id).
  - Supports merged, replaced, deleted, and gathered states.

version_added: "0.1.0"

author:
  - Cisco Meraki

options:
  serial:
    description: Device serial number.
    type: str
    required: true

  state:
    description: The state of the resource.
    type: str
    choices:
      - merged
      - replaced
      - overridden
      - deleted
      - gathered
    default: merged

  config:
    description: List of switch port configurations.
    type: list
    elements: dict
    suboptions:
      port_id:
        description: Port number/ID.
        type: str

      name:
        description: Port name.
        type: str

      tags:
        description: Tags for the port.
        type: list
        elements: str

      enabled:
        description: Whether the port is enabled.
        type: bool

      type:
        description: Port type.
        type: str
        choices:
          - access
          - trunk

      vlan:
        description: VLAN number.
        type: int

      voice_vlan:
        description: Voice VLAN number.
        type: int

      allowed_vlans:
        description: Allowed VLANs (for trunk ports).
        type: str

      poe_enabled:
        description: Power over Ethernet enabled.
        type: bool

      isolation_enabled:
        description: Port isolation enabled.
        type: bool

      rstp_enabled:
        description: RSTP enabled.
        type: bool

      stp_guard:
        description: STP guard setting.
        type: str
        choices:
          - disabled
          - root guard
          - bpdu guard
          - loop guard

      link_negotiation:
        description: Link speed negotiation.
        type: str

      port_schedule_id:
        description: Port schedule ID.
        type: str

      udld:
        description: Unidirectional Link Detection action.
        type: str
        choices:
          - Alert only
          - Enforce

      access_policy_type:
        description: Access policy type.
        type: str

      access_policy_number:
        description: Access policy number.
        type: int

      sticky_mac_allow_list:
        description: Sticky MAC allow list.
        type: list
        elements: str

      sticky_mac_allow_list_limit:
        description: Sticky MAC allow list limit.
        type: int

      storm_control_enabled:
        description: Storm control enabled.
        type: bool

      adaptive_policy_group_id:
        description: Adaptive policy group ID.
        type: str

      peer_sgt_capable:
        description: Peer SGT capable.
        type: bool

      flexible_stacking_enabled:
        description: Flexible stacking enabled.
        type: bool

      dai_trusted:
        description: DAI trusted.
        type: bool

      profile:
        description: Port profile.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki switch port configuration — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      name: Test-Config
      tags:
        - ansible
        - test
      enabled: true
      type: access
      vlan: 1
      voice_vlan: 100
      allowed_vlans: all

- name: Create switch_ports with merged state
  cisco.meraki_rm.meraki_switch_ports:
    serial: "Q2XX-XXXX-XXXX"
    state: merged
    config:
      - "{{ expected_config }}"
  register: merge_result

- name: Assert resource was created
  ansible.builtin.assert:
    that:
      - merge_result is changed
      - merge_result.config | length == 1

- name: Compare expected paths to result (subset check)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}"
  vars:
    expected_paths: "{{ expected_config | ansible.utils.to_paths }}"
    result_paths: "{{ merge_result.config[0] | ansible.utils.to_paths }}"

- name: Assert all expected fields are present and match
  ansible.builtin.assert:
    that: path_check.contained | bool
    success_msg: "{{ success_msg }}"
    fail_msg: "{{ fail_msg }}"
  vars:
    success_msg: "All expected fields match. Extras: {{ path_check.extras }}"
    fail_msg: "Missing or mismatch: {{ path_check.missing }}. Extras: {{ path_check.extras }}"

# Manage Meraki switch port configuration — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      name: Replaced-Config
      tags:
        - ansible
        - replaced
      enabled: false
      type: trunk
      vlan: 20
      voice_vlan: 100
      allowed_vlans: all

- name: Replace switch_ports configuration
  cisco.meraki_rm.meraki_switch_ports:
    serial: "Q2XX-XXXX-XXXX"
    state: replaced
    config:
      - "{{ expected_config }}"
  register: replace_result

- name: Assert resource was replaced
  ansible.builtin.assert:
    that:
      - replace_result is changed
      - replace_result.config | length == 1

- name: Compare expected paths to result (subset check)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}"
  vars:
    expected_paths: "{{ expected_config | ansible.utils.to_paths }}"
    result_paths: "{{ replace_result.config[0] | ansible.utils.to_paths }}"

- name: Assert all expected fields are present and match
  ansible.builtin.assert:
    that: path_check.contained | bool
    success_msg: "{{ success_msg }}"
    fail_msg: "{{ fail_msg }}"
  vars:
    success_msg: "All expected fields match. Extras: {{ path_check.extras }}"
    fail_msg: "Missing or mismatch: {{ path_check.missing }}. Extras: {{ path_check.extras }}"

# Manage Meraki switch port configuration — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      name: Replaced-Config
      tags:
        - ansible
        - replaced
      enabled: false
      type: trunk
      vlan: 20
      voice_vlan: 100
      allowed_vlans: all

- name: Override all switch_ports — desired state only
  cisco.meraki_rm.meraki_switch_ports:
    serial: "Q2XX-XXXX-XXXX"
    state: overridden
    config:
      - "{{ expected_config }}"
  register: override_result

- name: Assert resources were overridden
  ansible.builtin.assert:
    that:
      - override_result is changed
      - override_result.config | length == 1

- name: Compare expected paths to result (subset check)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | cisco.meraki_rm.path_contained_in(result_paths) }}"
  vars:
    expected_paths: "{{ expected_config | ansible.utils.to_paths }}"
    result_paths: "{{ override_result.config[0] | ansible.utils.to_paths }}"

- name: Assert all expected fields are present and match
  ansible.builtin.assert:
    that: path_check.contained | bool
    success_msg: "{{ success_msg }}"
    fail_msg: "{{ fail_msg }}"
  vars:
    success_msg: "All expected fields match. Extras: {{ path_check.extras }}"
    fail_msg: "Missing or mismatch: {{ path_check.missing }}. Extras: {{ path_check.extras }}"

# Manage Meraki switch port configuration — gather current configuration

- name: Gather current switch_ports configuration
  cisco.meraki_rm.meraki_switch_ports:
    serial: "Q2XX-XXXX-XXXX"
    state: gathered
  register: gathered

- name: Assert gathered config is not empty
  ansible.builtin.assert:
    that:
      - gathered.config is defined
      - gathered.config | length > 0
    fail_msg: "Gathered config is empty — expected at least one resource"

- name: Display gathered configuration
  ansible.builtin.debug:
    var: gathered.config

# Manage Meraki switch port configuration — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      port_schedule_id: example

- name: Delete switch_ports configuration
  cisco.meraki_rm.meraki_switch_ports:
    serial: "Q2XX-XXXX-XXXX"
    state: deleted
    config:
      - "{{ expected_config }}"
  register: delete_result

- name: Assert resource was deleted
  ansible.builtin.assert:
    that:
      - delete_result is changed
      - delete_result is not failed
'''

RETURN = r'''
config:
  description: The resulting resource configuration.
  type: list
  returned: always
'''

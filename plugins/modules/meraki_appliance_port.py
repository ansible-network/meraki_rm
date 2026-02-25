#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_port.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_port

short_description: Manage Meraki appliance ports

description:
  - Manage Meraki appliance ports for a network.
  - Read/update only (ports exist by default, no create/delete).
  - Supports merged, replaced, and gathered states.

version_added: "0.1.0"

author:
  - Cisco Meraki

options:
  network_id:
    description: The network ID.
    type: str
    required: true

  state:
    description: The state of the resource.
    type: str
    choices:
      - merged
      - replaced
      - gathered
    default: merged

  config:
    description: List of port configurations.
    type: list
    elements: dict
    suboptions:
      port_id:
        description: Port ID (e.g., 1, 2, 3, 4). Required for merged, replaced.
        type: str

      enabled:
        description: Whether the port is enabled.
        type: bool

      type:
        description: Port type (access or trunk).
        type: str
        choices:
          - access
          - trunk

      vlan:
        description: Native VLAN (trunk) or access VLAN.
        type: int

      allowed_vlans:
        description: Allowed VLANs (comma-delimited or 'all').
        type: str

      access_policy:
        description: Access policy name (access ports only).
        type: str

      drop_untagged_traffic:
        description: Drop untagged traffic (trunk ports).
        type: bool
'''

EXAMPLES = r'''
---
# Manage Meraki appliance ports — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      enabled: true
      type: access
      vlan: 1
      allowed_vlans: all
      access_policy: example
      drop_untagged_traffic: true

- name: Create appliance_port with merged state
  cisco.meraki_rm.meraki_appliance_port:
    network_id: "N_123456789012345678"
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

# Manage Meraki appliance ports — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      port_id: "1"
      enabled: false
      type: trunk
      vlan: 20
      allowed_vlans: all
      access_policy: example
      drop_untagged_traffic: true

- name: Replace appliance_port configuration
  cisco.meraki_rm.meraki_appliance_port:
    network_id: "N_123456789012345678"
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

# Manage Meraki appliance ports — gather current configuration

- name: Gather current appliance_port configuration
  cisco.meraki_rm.meraki_appliance_port:
    network_id: "N_123456789012345678"
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
'''

RETURN = r'''
config:
  description: The resulting resource configuration.
  type: list
  returned: always
'''

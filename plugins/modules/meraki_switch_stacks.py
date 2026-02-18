#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_stacks.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_stacks

short_description: Manage Meraki switch stacks

description:
  - Manage Meraki switch stacks for a network.
  - Network-scoped. Supports merged, replaced, deleted, and gathered states.

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
      - overridden
      - deleted
      - gathered
    default: merged

  config:
    description: List of switch stack configurations.
    type: list
    elements: dict
    suboptions:
      switch_stack_id:
        description: Switch stack ID (identifier).
        type: str

      name:
        description: Name of the switch stack.
        type: str

      serials:
        description: Serials of switches in the stack.
        type: list
        elements: str

      members:
        description: Members of the stack.
        type: list
        elements: dict

      is_monitor_only:
        description: Whether stack is monitor only.
        type: bool

      virtual_mac:
        description: Virtual MAC address of the switch stack.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki switch stacks — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      switch_stack_id: example
      name: Test-Config
      is_monitor_only: true
      virtual_mac: example

- name: Create switch_stacks with merged state
  cisco.meraki_rm.meraki_switch_stacks:
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

- name: Compare expected paths to result (subset: expected contained in result)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | path_contained_in(result_paths) }}"
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

# Manage Meraki switch stacks — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      switch_stack_id: example
      name: Replaced-Config
      is_monitor_only: true
      virtual_mac: example

- name: Replace switch_stacks configuration
  cisco.meraki_rm.meraki_switch_stacks:
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

- name: Compare expected paths to result (subset: expected contained in result)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | path_contained_in(result_paths) }}"
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

# Manage Meraki switch stacks — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      switch_stack_id: example
      name: Replaced-Config
      is_monitor_only: true
      virtual_mac: example

- name: Override all switch_stacks — desired state only
  cisco.meraki_rm.meraki_switch_stacks:
    network_id: "N_123456789012345678"
    state: overridden
    config:
      - "{{ expected_config }}"
  register: override_result

- name: Assert resources were overridden
  ansible.builtin.assert:
    that:
      - override_result is changed
      - override_result.config | length == 1

- name: Compare expected paths to result (subset: expected contained in result)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | path_contained_in(result_paths) }}"
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

# Manage Meraki switch stacks — gather current configuration

- name: Gather current switch_stacks configuration
  cisco.meraki_rm.meraki_switch_stacks:
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

# Manage Meraki switch stacks — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      switch_stack_id: example

- name: Delete switch_stacks configuration
  cisco.meraki_rm.meraki_switch_stacks:
    network_id: "N_123456789012345678"
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

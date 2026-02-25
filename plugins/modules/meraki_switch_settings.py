#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_settings.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_settings

short_description: Manage Meraki switch settings (MTU, storm control, DSCP, AMI, general)

description:
  - Manage Meraki switch settings for a network (consolidated).
  - Singleton per network (MTU, storm control, DSCP, AMI, general).
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
    description: Switch settings configuration (singleton).
    type: list
    elements: dict
    suboptions:
      default_mtu_size:
        description: MTU size for the entire network.
        type: int

      overrides:
        description: Override MTU for individual switches.
        type: list
        elements: dict

      broadcast_threshold:
        description: Broadcast storm control threshold.
        type: int

      multicast_threshold:
        description: Multicast storm control threshold.
        type: int

      unknown_unicast_threshold:
        description: Unknown unicast storm control threshold.
        type: int

      mappings:
        description: DSCP to CoS mappings.
        type: list
        elements: dict

      use_combined_power:
        description: Use combined power for secondary power supplies.
        type: bool

      power_exceptions:
        description: Per-switch power exceptions.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki switch settings (MTU, storm control, DSCP, AMI, general) — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      default_mtu_size: 1
      broadcast_threshold: 1
      multicast_threshold: 1
      unknown_unicast_threshold: 1
      use_combined_power: true

- name: Create switch_settings with merged state
  cisco.meraki_rm.meraki_switch_settings:
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

# Manage Meraki switch settings (MTU, storm control, DSCP, AMI, general) — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      default_mtu_size: 1
      broadcast_threshold: 1
      multicast_threshold: 1
      unknown_unicast_threshold: 1
      use_combined_power: true

- name: Replace switch_settings configuration
  cisco.meraki_rm.meraki_switch_settings:
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

# Manage Meraki switch settings (MTU, storm control, DSCP, AMI, general) — gather current configuration

- name: Gather current switch_settings configuration
  cisco.meraki_rm.meraki_switch_settings:
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

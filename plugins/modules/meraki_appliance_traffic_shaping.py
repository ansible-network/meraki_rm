#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_traffic_shaping.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_traffic_shaping

short_description: Manage Meraki appliance traffic shaping

description:
  - Manage Meraki appliance traffic shaping for a network.
  - Singleton per network (update only, no create/delete).
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
    description: Traffic shaping configuration (singleton).
    type: list
    elements: dict
    suboptions:
      default_rules_enabled:
        description: Whether default traffic shaping rules are enabled.
        type: bool

      default_uplink:
        description: The default uplink (e.g., wan1, wan2).
        type: str

      rules:
        description: Array of traffic shaping rules.
        type: list
        elements: dict

      bandwidth_limits:
        description: Uplink bandwidth limits by interface.
        type: dict

      global_bandwidth_limits:
        description: Global per-client bandwidth limit.
        type: dict

      failover_and_failback:
        description: WAN failover and failback settings.
        type: dict

      load_balancing_enabled:
        description: Whether load balancing is enabled.
        type: bool

      active_active_auto_vpn_enabled:
        description: Whether active-active AutoVPN is enabled.
        type: bool

      vpn_traffic_uplink_preferences:
        description: Uplink preference rules for VPN traffic.
        type: list
        elements: dict

      wan_traffic_uplink_preferences:
        description: Uplink preference rules for WAN traffic.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki appliance traffic shaping — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      default_rules_enabled: true
      default_uplink: example
      load_balancing_enabled: true
      active_active_auto_vpn_enabled: true

- name: Create appliance_traffic_shaping with merged state
  cisco.meraki_rm.meraki_appliance_traffic_shaping:
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

# Manage Meraki appliance traffic shaping — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      default_rules_enabled: true
      default_uplink: example
      load_balancing_enabled: true
      active_active_auto_vpn_enabled: true

- name: Replace appliance_traffic_shaping configuration
  cisco.meraki_rm.meraki_appliance_traffic_shaping:
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

# Manage Meraki appliance traffic shaping — gather current configuration

- name: Gather current appliance_traffic_shaping configuration
  cisco.meraki_rm.meraki_appliance_traffic_shaping:
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

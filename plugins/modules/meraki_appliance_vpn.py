#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_vpn.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_vpn

short_description: Manage Meraki appliance site-to-site VPN

description:
  - Manage Meraki appliance site-to-site VPN for a network.
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
    description: VPN configuration (singleton).
    type: list
    elements: dict
    suboptions:
      mode:
        description: Site-to-site VPN mode.
        type: str
        choices:
          - none
          - spoke
          - hub

      hubs:
        description: List of VPN hubs, in order of preference.
        type: list
        elements: dict

      subnets:
        description: List of subnets and their VPN presence.
        type: list
        elements: dict

      subnet:
        description: Configuration of subnet features.
        type: dict

      enabled:
        description: Whether VPN is enabled.
        type: bool

      as_number:
        description: BGP autonomous system number.
        type: int

      ibgp_hold_timer:
        description: iBGP hold time in seconds.
        type: int

      neighbors:
        description: List of eBGP neighbor configurations.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki appliance site-to-site VPN — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      mode: none
      subnet: 192.168.128.0/24
      enabled: true
      as_number: 1
      ibgp_hold_timer: 1

- name: Create appliance_vpn with merged state
  cisco.meraki_rm.meraki_appliance_vpn:
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

# Manage Meraki appliance site-to-site VPN — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      mode: spoke
      subnet: 10.20.0.0/24
      enabled: false
      as_number: 1
      ibgp_hold_timer: 1

- name: Replace appliance_vpn configuration
  cisco.meraki_rm.meraki_appliance_vpn:
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

# Manage Meraki appliance site-to-site VPN — gather current configuration

- name: Gather current appliance_vpn configuration
  cisco.meraki_rm.meraki_appliance_vpn:
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

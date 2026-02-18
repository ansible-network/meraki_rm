#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_dhcp_policy.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_dhcp_policy

short_description: Manage Meraki switch DHCP server policy

description:
  - Manage Meraki switch DHCP server policy for a network.
  - Singleton per network (GET/PUT settings).
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
    description: DHCP policy configuration (singleton).
    type: list
    elements: dict
    suboptions:
      default_policy:
        description: Default policy for new DHCP servers (allow or block).
        type: str

      allowed_servers:
        description: MAC addresses of DHCP servers to permit.
        type: list
        elements: str

      blocked_servers:
        description: MAC addresses of DHCP servers to block.
        type: list
        elements: str

      always_allowed_servers:
        description: MAC addresses always allowed on the network.
        type: list
        elements: str

      arp_inspection:
        description: Dynamic ARP Inspection settings.
        type: dict

      alerts:
        description: Email alert settings for DHCP servers.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki switch DHCP server policy — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      default_policy: example

- name: Create switch_dhcp_policy with merged state
  cisco.meraki_rm.meraki_switch_dhcp_policy:
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

# Manage Meraki switch DHCP server policy — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      default_policy: example

- name: Replace switch_dhcp_policy configuration
  cisco.meraki_rm.meraki_switch_dhcp_policy:
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

# Manage Meraki switch DHCP server policy — gather current configuration

- name: Gather current switch_dhcp_policy configuration
  cisco.meraki_rm.meraki_switch_dhcp_policy:
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

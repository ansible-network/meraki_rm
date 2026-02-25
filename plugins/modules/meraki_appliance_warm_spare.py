#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_warm_spare.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_warm_spare

short_description: Manage Meraki appliance warm spare

description:
  - Manage Meraki appliance warm spare configuration for a network.
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
    description: Warm spare configuration (singleton).
    type: list
    elements: dict
    suboptions:
      enabled:
        description: Whether warm spare is enabled.
        type: bool

      spare_serial:
        description: Serial number of the warm spare appliance.
        type: str

      uplink_mode:
        description: Uplink mode (virtual or public).
        type: str

      virtual_ip1:
        description: WAN 1 shared IP.
        type: str

      virtual_ip2:
        description: WAN 2 shared IP.
        type: str

      wan1:
        description: WAN 1 IP and subnet.
        type: dict

      wan2:
        description: WAN 2 IP and subnet.
        type: dict

      primary_serial:
        description: Serial number of the primary appliance.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki appliance warm spare — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: true
      spare_serial: Q2XX-SPARE-0001
      uplink_mode: virtual
      virtual_ip1: 10.0.0.2
      virtual_ip2: 10.0.0.3
      primary_serial: example

- name: Create appliance_warm_spare with merged state
  cisco.meraki_rm.meraki_appliance_warm_spare:
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

# Manage Meraki appliance warm spare — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: false
      spare_serial: Q2XX-SPARE-0001
      uplink_mode: virtual
      virtual_ip1: 10.0.0.2
      virtual_ip2: 10.0.0.3
      primary_serial: example

- name: Replace appliance_warm_spare configuration
  cisco.meraki_rm.meraki_appliance_warm_spare:
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

# Manage Meraki appliance warm spare — gather current configuration

- name: Gather current appliance_warm_spare configuration
  cisco.meraki_rm.meraki_appliance_warm_spare:
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

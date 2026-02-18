#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_device_management_interface.py for the implementation.

DOCUMENTATION = r'''
module: meraki_device_management_interface

short_description: Manage Meraki device management interface

description:
  - Manage Meraki device management interface (singleton per device).
  - Supports merged, replaced, and gathered states.

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
      - gathered
    default: merged

  config:
    description: Management interface configuration (singleton).
    type: list
    elements: dict
    suboptions:
      wan1:
        description: WAN 1 settings.
        type: dict

      wan2:
        description: WAN 2 settings (MX devices only).
        type: dict

      ddns_hostnames:
        description: Dynamic DNS hostnames.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki device management interface — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Create device_management_interface with merged state
  cisco.meraki_rm.meraki_device_management_interface:
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

# Manage Meraki device management interface — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Replace device_management_interface configuration
  cisco.meraki_rm.meraki_device_management_interface:
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

# Manage Meraki device management interface — gather current configuration

- name: Gather current device_management_interface configuration
  cisco.meraki_rm.meraki_device_management_interface:
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
'''

RETURN = r'''
config:
  description: The resulting resource configuration.
  type: list
  returned: always
'''

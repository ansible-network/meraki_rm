#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_device.py for the implementation.

DOCUMENTATION = r'''
module: meraki_device

short_description: Manage Meraki device attributes

description:
  - Manage Meraki device attributes (read/update only, no create/delete).
  - Scope is device serial (one device per task).
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
    description: Device configuration (one device per task).
    type: list
    elements: dict
    suboptions:
      name:
        description: Name of the device.
        type: str

      tags:
        description: List of tags for the device.
        type: list
        elements: str

      lat:
        description: Latitude of the device.
        type: float

      lng:
        description: Longitude of the device.
        type: float

      address:
        description: Physical address of the device.
        type: str

      notes:
        description: Notes for the device (max 255 chars).
        type: str

      move_map_marker:
        description: Set lat/lng from address.
        type: bool

      floor_plan_id:
        description: Floor plan to associate with the device.
        type: str

      switch_profile_id:
        description: Switch template ID to bind to the device.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki device attributes — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Test-Config
      tags:
        - ansible
        - test
      lat: 37.7749
      lng: -122.4194
      address: 500 Terry Francine Street
      notes: example
      move_map_marker: true
      floor_plan_id: example

- name: Create device with merged state
  cisco.meraki_rm.meraki_device:
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

# Manage Meraki device attributes — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Replaced-Config
      tags:
        - ansible
        - replaced
      lat: 37.7749
      lng: -122.4194
      address: 500 Terry Francine Street
      notes: example
      move_map_marker: true
      floor_plan_id: example

- name: Replace device configuration
  cisco.meraki_rm.meraki_device:
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

# Manage Meraki device attributes — gather current configuration

- name: Gather current device configuration
  cisco.meraki_rm.meraki_device:
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

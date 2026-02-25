#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_floor_plans.py for the implementation.

DOCUMENTATION = r'''
module: meraki_floor_plans

short_description: Manage Meraki floor plans

description:
  - Manage Meraki floor plans for a network.
  - Supports merged, replaced, deleted, and gathered states.

notes:
  - "Canonical key: C(name) — identifies the resource in playbooks."
  - "System key: C(floor_plan_id) — server-assigned, resolved automatically from gathered state."
  - "Users do not need to provide C(floor_plan_id) unless disambiguating duplicate names."

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
    description: List of floor plan configurations.
    type: list
    elements: dict
    suboptions:
      floor_plan_id:
        description:
          - Server-assigned ID, resolved automatically by matching on C(name).
          - Provide only to disambiguate when duplicate names exist.
        type: str

      name:
        description: Name of the floor plan.
        type: str

      center:
        description: Center coordinates (lat/lng) of the floor plan.
        type: dict

      bottom_left_corner:
        description: Bottom left corner coordinates.
        type: dict

      bottom_right_corner:
        description: Bottom right corner coordinates.
        type: dict

      top_left_corner:
        description: Top left corner coordinates.
        type: dict

      top_right_corner:
        description: Top right corner coordinates.
        type: dict

      width:
        description: Width of the floor plan.
        type: float

      height:
        description: Height of the floor plan.
        type: float

      floor_number:
        description: Floor number within the building.
        type: float

      image_contents:
        description: Base64 encoded floor plan image.
        type: str

      image_extension:
        description: Image format (e.g., png, jpg).
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki floor plans — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Test-Config
      width: 0.0
      height: 0.0
      floor_number: 0.0
      image_contents: example
      image_extension: example

- name: Create floor_plans with merged state
  cisco.meraki_rm.meraki_floor_plans:
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

# Manage Meraki floor plans — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Replaced-Config
      width: 0.0
      height: 0.0
      floor_number: 0.0
      image_contents: example
      image_extension: example

- name: Replace floor_plans configuration
  cisco.meraki_rm.meraki_floor_plans:
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

# Manage Meraki floor plans — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Replaced-Config
      width: 0.0
      height: 0.0
      floor_number: 0.0
      image_contents: example
      image_extension: example

- name: Override all floor_plans — desired state only
  cisco.meraki_rm.meraki_floor_plans:
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

# Manage Meraki floor plans — gather current configuration

- name: Gather current floor_plans configuration
  cisco.meraki_rm.meraki_floor_plans:
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

# Manage Meraki floor plans — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      name: Test-Config

- name: Delete floor_plans configuration
  cisco.meraki_rm.meraki_floor_plans:
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

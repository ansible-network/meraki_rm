#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_rf_profiles.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_rf_profiles

short_description: Manage Meraki appliance RF profiles

description:
  - Manage Meraki appliance RF profiles for a network.
  - Supports merged, replaced, deleted, and gathered states.

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
    description: List of RF profile configurations.
    type: list
    elements: dict
    suboptions:
      rf_profile_id:
        description: RF profile ID. Required for merged, replaced, deleted.
        type: str

      name:
        description: Name of the profile. Required for create.
        type: str

      two_four_ghz_settings:
        description: Settings for 2.4GHz band.
        type: dict

      five_ghz_settings:
        description: Settings for 5GHz band.
        type: dict

      per_ssid_settings:
        description: Per-SSID radio settings by number.
        type: dict

      assigned:
        description: Assigned RF profiles.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki appliance RF profiles — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      rf_profile_id: example
      name: Test-Config

- name: Create appliance_rf_profiles with merged state
  cisco.meraki_rm.meraki_appliance_rf_profiles:
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

# Manage Meraki appliance RF profiles — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      rf_profile_id: example
      name: Replaced-Config

- name: Replace appliance_rf_profiles configuration
  cisco.meraki_rm.meraki_appliance_rf_profiles:
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

# Manage Meraki appliance RF profiles — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      rf_profile_id: example
      name: Replaced-Config

- name: Override all appliance_rf_profiles — desired state only
  cisco.meraki_rm.meraki_appliance_rf_profiles:
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

# Manage Meraki appliance RF profiles — gather current configuration

- name: Gather current appliance_rf_profiles configuration
  cisco.meraki_rm.meraki_appliance_rf_profiles:
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

# Manage Meraki appliance RF profiles — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      rf_profile_id: example

- name: Delete appliance_rf_profiles configuration
  cisco.meraki_rm.meraki_appliance_rf_profiles:
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

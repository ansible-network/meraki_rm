#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_wireless_air_marshal_rules.py for the implementation.

DOCUMENTATION = r'''
module: meraki_wireless_air_marshal_rules

short_description: Manage Meraki wireless Air Marshal (rogue AP detection)

description:
  - Manage Meraki wireless Air Marshal rules and settings for a network.
  - Mixed resource - rules (CRUD) and settings (singleton).
  - Supports merged, replaced, deleted, and gathered states.

notes:
  - "This resource has no canonical key (Category C — gather-first)."
  - "Use C(state=gathered) to discover C(rule_id) values, then reference them in subsequent tasks."

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
    description: List of Air Marshal rule configurations.
    type: list
    elements: dict
    suboptions:
      rule_id:
        description:
          - Server-assigned rule ID. Discover via C(state=gathered).
        type: str

      type:
        description: Rule type (allow, block, or alert).
        type: str

      match:
        description: Rule specification/match criteria.
        type: dict

      default_policy:
        description: Default policy for rogue networks.
        type: str

      ssid:
        description: SSID name for the rule.
        type: str

      bssids:
        description: BSSIDs broadcasting the SSID.
        type: list
        elements: dict

      channels:
        description: Channels where SSID was observed.
        type: list
        elements: int
'''

EXAMPLES = r'''
---
# Manage Meraki wireless Air Marshal (rogue AP detection) — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      default_policy: example
      ssid: example

- name: Create wireless_air_marshal_rules with merged state
  cisco.meraki_rm.meraki_wireless_air_marshal_rules:
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

# Manage Meraki wireless Air Marshal (rogue AP detection) — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      default_policy: example
      ssid: example

- name: Replace wireless_air_marshal_rules configuration
  cisco.meraki_rm.meraki_wireless_air_marshal_rules:
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

# Manage Meraki wireless Air Marshal (rogue AP detection) — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      default_policy: example
      ssid: example

- name: Override all wireless_air_marshal_rules — desired state only
  cisco.meraki_rm.meraki_wireless_air_marshal_rules:
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

# Manage Meraki wireless Air Marshal (rogue AP detection) — gather current configuration

- name: Gather current wireless_air_marshal_rules configuration
  cisco.meraki_rm.meraki_wireless_air_marshal_rules:
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

# Manage Meraki wireless Air Marshal (rogue AP detection) — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      rule_id: example

- name: Delete wireless_air_marshal_rules configuration
  cisco.meraki_rm.meraki_wireless_air_marshal_rules:
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

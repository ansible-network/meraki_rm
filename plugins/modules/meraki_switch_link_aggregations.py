#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_link_aggregations.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_link_aggregations

short_description: Manage Meraki switch link aggregations

description:
  - Manage Meraki switch link aggregation groups for a network.
  - Network-scoped. Supports merged, replaced, deleted, and gathered states.

notes:
  - "This resource has no canonical key (Category C — gather-first)."
  - "Use C(state=gathered) to discover C(link_aggregation_id) values, then reference them in subsequent tasks."

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
    description: List of link aggregation configurations.
    type: list
    elements: dict
    suboptions:
      link_aggregation_id:
        description:
          - Server-assigned aggregation ID. Discover via C(state=gathered).
        type: str

      switch_ports:
        description: Array of switch ports for the aggregation.
        type: list
        elements: dict

      switch_profile_ports:
        description: Array of switch profile ports for creating aggregation.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki switch link aggregations — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Create switch_link_aggregations with merged state
  cisco.meraki_rm.meraki_switch_link_aggregations:
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

# Manage Meraki switch link aggregations — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Replace switch_link_aggregations configuration
  cisco.meraki_rm.meraki_switch_link_aggregations:
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

# Manage Meraki switch link aggregations — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Override all switch_link_aggregations — desired state only
  cisco.meraki_rm.meraki_switch_link_aggregations:
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

# Manage Meraki switch link aggregations — gather current configuration

- name: Gather current switch_link_aggregations configuration
  cisco.meraki_rm.meraki_switch_link_aggregations:
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

# Manage Meraki switch link aggregations — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      link_aggregation_id: example

- name: Delete switch_link_aggregations configuration
  cisco.meraki_rm.meraki_switch_link_aggregations:
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

#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_wireless_ethernet_port_profiles.py for the implementation.

DOCUMENTATION = r'''
module: meraki_wireless_ethernet_port_profiles

short_description: Manage Meraki wireless Ethernet port profiles

description:
  - Manage Meraki wireless AP Ethernet port profiles for a network.
  - Network-scoped. Supports merged, replaced, deleted, and gathered states.

notes:
  - "Canonical key: C(name) — identifies the resource in playbooks."
  - "System key: C(profile_id) — server-assigned, resolved automatically from gathered state."
  - "Users do not need to provide C(profile_id) unless disambiguating duplicate names."

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
    description: List of Ethernet port profile configurations.
    type: list
    elements: dict
    suboptions:
      profile_id:
        description:
          - Server-assigned ID, resolved automatically by matching on C(name).
          - Provide only to disambiguate when duplicate names exist.
        type: str

      name:
        description: AP port profile name.
        type: str

      ports:
        description: Ports configuration.
        type: list
        elements: dict

      usb_ports:
        description: USB ports configuration.
        type: list
        elements: dict

      is_default:
        description: Whether this is the default profile.
        type: bool

      serials:
        description: List of AP serials to assign.
        type: list
        elements: str
'''

EXAMPLES = r'''
---
# Manage Meraki wireless Ethernet port profiles — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Test-Config
      is_default: true

- name: Create wireless_ethernet_port_profiles with merged state
  cisco.meraki_rm.meraki_wireless_ethernet_port_profiles:
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

# Manage Meraki wireless Ethernet port profiles — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Replaced-Config
      is_default: true

- name: Replace wireless_ethernet_port_profiles configuration
  cisco.meraki_rm.meraki_wireless_ethernet_port_profiles:
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

# Manage Meraki wireless Ethernet port profiles — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      name: Replaced-Config
      is_default: true

- name: Override all wireless_ethernet_port_profiles — desired state only
  cisco.meraki_rm.meraki_wireless_ethernet_port_profiles:
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

# Manage Meraki wireless Ethernet port profiles — gather current configuration

- name: Gather current wireless_ethernet_port_profiles configuration
  cisco.meraki_rm.meraki_wireless_ethernet_port_profiles:
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

# Manage Meraki wireless Ethernet port profiles — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      name: Test-Config

- name: Delete wireless_ethernet_port_profiles configuration
  cisco.meraki_rm.meraki_wireless_ethernet_port_profiles:
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

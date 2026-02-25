#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_network_settings.py for the implementation.

DOCUMENTATION = r'''
module: meraki_network_settings

short_description: Manage Meraki network settings

description:
  - Manage Meraki network settings (singleton per network).
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
    description: Network settings configuration (singleton).
    type: list
    elements: dict
    suboptions:
      local_status_page_enabled:
        description: Enable local device status pages.
        type: bool

      remote_status_page_enabled:
        description: Enable access to device status page via LAN IP.
        type: bool

      local_status_page:
        description: Local status page authentication options.
        type: dict

      fips:
        description: FIPS options for the network.
        type: dict

      named_vlans:
        description: Named VLANs options.
        type: dict

      secure_port:
        description: SecureConnect options.
        type: dict

      reporting_enabled:
        description: Enable NetFlow traffic reporting.
        type: bool

      mode:
        description: Traffic analysis mode.
        type: str

      custom_pie_chart_items:
        description: Custom pie chart items for traffic reporting.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki network settings — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      local_status_page_enabled: true
      remote_status_page_enabled: true
      reporting_enabled: true
      mode: none

- name: Create network_settings with merged state
  cisco.meraki_rm.meraki_network_settings:
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

# Manage Meraki network settings — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      local_status_page_enabled: true
      remote_status_page_enabled: true
      reporting_enabled: true
      mode: spoke

- name: Replace network_settings configuration
  cisco.meraki_rm.meraki_network_settings:
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

# Manage Meraki network settings — gather current configuration

- name: Gather current network_settings configuration
  cisco.meraki_rm.meraki_network_settings:
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

#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_ssid.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_ssid

short_description: Manage Meraki appliance SSIDs

description:
  - Manage Meraki appliance SSIDs (MX wireless) for a network.
  - Read/update only (SSIDs 0-4 exist by default, no create/delete).
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
    description: List of appliance SSID configurations.
    type: list
    elements: dict
    suboptions:
      number:
        description: SSID number (0-4). Required for merged, replaced.
        type: int

      name:
        description: Name of the SSID.
        type: str

      enabled:
        description: Whether the SSID is enabled.
        type: bool

      auth_mode:
        description: Association control method.
        type: str

      encryption_mode:
        description: PSK encryption mode.
        type: str

      psk:
        description: Passkey (auth_mode is psk).
        type: str

      default_vlan_id:
        description: VLAN ID associated with this SSID.
        type: int

      visible:
        description: Whether to advertise or hide this SSID.
        type: bool

      wpa_encryption_mode:
        description: WPA encryption mode.
        type: str

      radius_servers:
        description: RADIUS 802.1x servers for authentication.
        type: list
        elements: dict
'''

EXAMPLES = r'''
---
# Manage Meraki appliance SSIDs — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      number: 1
      name: Test-Config
      enabled: true
      auth_mode: open
      encryption_mode: wpa
      psk: testpassword123
      default_vlan_id: 1
      visible: true

- name: Create appliance_ssid with merged state
  cisco.meraki_rm.meraki_appliance_ssid:
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

# Manage Meraki appliance SSIDs — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      number: 1
      name: Replaced-Config
      enabled: false
      auth_mode: open
      encryption_mode: wpa
      psk: testpassword123
      default_vlan_id: 1
      visible: true

- name: Replace appliance_ssid configuration
  cisco.meraki_rm.meraki_appliance_ssid:
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

# Manage Meraki appliance SSIDs — gather current configuration

- name: Gather current appliance_ssid configuration
  cisco.meraki_rm.meraki_appliance_ssid:
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

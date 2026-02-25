#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_switch_routing.py for the implementation.

DOCUMENTATION = r'''
module: meraki_switch_routing

short_description: Manage Meraki switch routing (multicast and OSPF)

description:
  - Manage Meraki switch routing configuration for a network.
  - Singleton per network (multicast + OSPF settings).
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
    description: Switch routing configuration (singleton).
    type: list
    elements: dict
    suboptions:
      default_settings:
        description: Default multicast settings for the network.
        type: dict

      overrides:
        description: Multicast overrides per switch/stack/profile.
        type: list
        elements: dict

      enabled:
        description: Enable OSPF routing.
        type: bool

      hello_timer_in_seconds:
        description: OSPF hello timer in seconds.
        type: int

      dead_timer_in_seconds:
        description: OSPF dead timer in seconds.
        type: int

      areas:
        description: OSPF areas.
        type: list
        elements: dict

      md5_authentication_enabled:
        description: Enable MD5 authentication for OSPF.
        type: bool

      md5_authentication_key:
        description: MD5 authentication credentials.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki switch routing (multicast and OSPF) — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: true
      hello_timer_in_seconds: 1
      dead_timer_in_seconds: 1
      md5_authentication_enabled: true

- name: Create switch_routing with merged state
  cisco.meraki_rm.meraki_switch_routing:
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

# Manage Meraki switch routing (multicast and OSPF) — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: false
      hello_timer_in_seconds: 1
      dead_timer_in_seconds: 1
      md5_authentication_enabled: true

- name: Replace switch_routing configuration
  cisco.meraki_rm.meraki_switch_routing:
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

# Manage Meraki switch routing (multicast and OSPF) — gather current configuration

- name: Gather current switch_routing configuration
  cisco.meraki_rm.meraki_switch_routing:
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

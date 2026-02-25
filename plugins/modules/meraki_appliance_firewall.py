#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_firewall.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_firewall

short_description: Manage Meraki appliance firewall rules

description:
  - Manage Meraki appliance L3 firewall rules for a network.
  - Singleton per network (update only, no create/delete).
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
    description: Firewall configuration (singleton).
    type: list
    elements: dict
    suboptions:
      rules:
        description: Ordered array of L3 firewall rules.
        type: list
        elements: dict

      syslog_default_rule:
        description: Log the special default rule.
        type: bool

      spoofing_protection:
        description: Spoofing protection settings.
        type: dict

      application_categories:
        description: L7 application categories and applications.
        type: list
        elements: dict

      access:
        description: Rule for which IPs are allowed to access.
        type: str

      allowed_ips:
        description: Array of allowed CIDRs.
        type: list
        elements: str

      service:
        description: Appliance service name.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki appliance firewall rules — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      syslog_default_rule: true
      access: example
      service: example

- name: Create appliance_firewall with merged state
  cisco.meraki_rm.meraki_appliance_firewall:
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

# Manage Meraki appliance firewall rules — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      syslog_default_rule: true
      access: example
      service: example

- name: Replace appliance_firewall configuration
  cisco.meraki_rm.meraki_appliance_firewall:
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

# Manage Meraki appliance firewall rules — gather current configuration

- name: Gather current appliance_firewall configuration
  cisco.meraki_rm.meraki_appliance_firewall:
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

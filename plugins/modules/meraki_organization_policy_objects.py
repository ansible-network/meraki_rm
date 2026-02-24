#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_policy_objects.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_policy_objects

short_description: Manage Meraki organization policy objects

description:
  - Manage Meraki organization policy objects.
  - Supports merged, replaced, overridden, deleted, and gathered states.

version_added: "0.1.0"

author:
  - Cisco Meraki

options:
  organization_id:
    description: The organization ID.
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
    description: List of policy object configurations.
    type: list
    elements: dict
    suboptions:
      policy_object_id:
        description: Policy object ID (for update/delete).
        type: str

      name:
        description: Name of the policy object.
        type: str

      category:
        description: Category of policy object.
        type: str
        choices:
          - adaptivePolicy
          - network

      type:
        description: Type of policy object.
        type: str
        choices:
          - adaptivePolicyIpv4Cidr
          - cidr
          - fqdn
          - ipAndMask

      cidr:
        description: CIDR value (for cidr type).
        type: str

      fqdn:
        description: Fully qualified domain name (for fqdn type).
        type: str

      ip:
        description: IP address (for ipAndMask type).
        type: str

      mask:
        description: Subnet mask (for ipAndMask type).
        type: str

      group_ids:
        description: IDs of policy object groups this object belongs to.
        type: list
        elements: str
'''

EXAMPLES = r'''
---
# Manage Meraki organization policy objects — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      policy_object_id: example
      name: Test-Config
      category: adaptivePolicy
      type: adaptivePolicyIpv4Cidr
      cidr: 192.168.128.0/24
      fqdn: example.com
      ip: 10.0.0.1
      mask: 24

- name: Create organization_policy_objects with merged state
  cisco.meraki_rm.meraki_organization_policy_objects:
    organization_id: "123456"
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

# Manage Meraki organization policy objects — gather current configuration

- name: Gather current organization_policy_objects configuration
  cisco.meraki_rm.meraki_organization_policy_objects:
    organization_id: "123456"
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

# Manage Meraki organization policy objects — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      policy_object_id: example

- name: Delete organization_policy_objects configuration
  cisco.meraki_rm.meraki_organization_policy_objects:
    organization_id: "123456"
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

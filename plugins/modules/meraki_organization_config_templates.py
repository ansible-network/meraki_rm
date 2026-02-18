#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_config_templates.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_config_templates

short_description: Manage Meraki organization configuration templates

description:
  - Manage Meraki organization configuration templates.
  - Supports merged, deleted, and gathered states.

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
      - deleted
      - gathered
    default: merged

  config:
    description: List of configuration template configurations.
    type: list
    elements: dict
    suboptions:
      config_template_id:
        description: Configuration template ID (for update/delete).
        type: str

      name:
        description: Name of the configuration template.
        type: str

      product_types:
        description: Product types (e.g. wireless, switch, appliance).
        type: list
        elements: str

      time_zone:
        description: Timezone of the configuration template.
        type: str

      copy_from_network_id:
        description: Network or template ID to copy configuration from.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki organization configuration templates — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      config_template_id: example
      name: Test-Config
      time_zone: example
      copy_from_network_id: example

- name: Create organization_config_templates with merged state
  cisco.meraki_rm.meraki_organization_config_templates:
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

# Manage Meraki organization configuration templates — gather current configuration

- name: Gather current organization_config_templates configuration
  cisco.meraki_rm.meraki_organization_config_templates:
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

# Manage Meraki organization configuration templates — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      config_template_id: example
      copy_from_network_id: example

- name: Delete organization_config_templates configuration
  cisco.meraki_rm.meraki_organization_config_templates:
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

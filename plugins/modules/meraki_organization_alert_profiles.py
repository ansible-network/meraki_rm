#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_alert_profiles.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_alert_profiles

short_description: Manage Meraki organization alert profiles

description:
  - Manage Meraki organization alert profiles.
  - Supports merged, replaced, overridden, deleted, and gathered states.

notes:
  - "This resource has no canonical key (Category C — gather-first)."
  - "Use C(state=gathered) to discover C(alert_config_id) values, then reference them in subsequent tasks."

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
    description: List of alert profile configurations.
    type: list
    elements: dict
    suboptions:
      alert_config_id:
        description:
          - Server-assigned config ID. Discover via C(state=gathered).
        type: str

      type:
        description: The alert type.
        type: str

      enabled:
        description: Whether the alert is enabled.
        type: bool

      alert_condition:
        description: Conditions that determine if the alert triggers.
        type: dict

      recipients:
        description: Recipients that receive the alert.
        type: dict

      network_tags:
        description: Network tags to monitor for the alert.
        type: list
        elements: str

      description:
        description: User-supplied description of the alert.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki organization alert profiles — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      enabled: true
      description: Managed by Ansible

- name: Create organization_alert_profiles with merged state
  cisco.meraki_rm.meraki_organization_alert_profiles:
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

# Manage Meraki organization alert profiles — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      enabled: false
      description: Replaced by Ansible

- name: Replace organization_alert_profiles configuration
  cisco.meraki_rm.meraki_organization_alert_profiles:
    organization_id: "123456"
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

# Manage Meraki organization alert profiles — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      type: access
      enabled: false
      description: Replaced by Ansible

- name: Override all organization_alert_profiles — desired state only
  cisco.meraki_rm.meraki_organization_alert_profiles:
    organization_id: "123456"
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

# Manage Meraki organization alert profiles — gather current configuration

- name: Gather current organization_alert_profiles configuration
  cisco.meraki_rm.meraki_organization_alert_profiles:
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

# Manage Meraki organization alert profiles — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      alert_config_id: example

- name: Delete organization_alert_profiles configuration
  cisco.meraki_rm.meraki_organization_alert_profiles:
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

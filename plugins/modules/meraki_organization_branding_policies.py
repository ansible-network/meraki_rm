#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_branding_policies.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_branding_policies

short_description: Manage Meraki organization branding policies

description:
  - Manage Meraki organization branding policies.
  - Supports merged, replaced, overridden, deleted, and gathered states.

notes:
  - "Canonical key: C(name) — identifies the resource in playbooks."
  - "System key: C(branding_policy_id) — server-assigned, resolved automatically from gathered state."
  - "Users do not need to provide C(branding_policy_id) unless disambiguating duplicate names."

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
    description: List of branding policy configurations.
    type: list
    elements: dict
    suboptions:
      branding_policy_id:
        description:
          - Server-assigned ID, resolved automatically by matching on C(name).
          - Provide only to disambiguate when duplicate names exist.
        type: str

      name:
        description: Name of the branding policy.
        type: str

      enabled:
        description: Whether the policy is enabled.
        type: bool

      admin_settings:
        description: Settings for which kinds of admins this policy applies to.
        type: dict

      help_settings:
        description: Modifications to Help page features.
        type: dict

      custom_logo:
        description: Custom logo properties.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki organization branding policies — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      branding_policy_id: example
      name: Test-Config
      enabled: true

- name: Create organization_branding_policies with merged state
  cisco.meraki_rm.meraki_organization_branding_policies:
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

# Manage Meraki organization branding policies — gather current configuration

- name: Gather current organization_branding_policies configuration
  cisco.meraki_rm.meraki_organization_branding_policies:
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

# Manage Meraki organization branding policies — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      branding_policy_id: example

- name: Delete organization_branding_policies configuration
  cisco.meraki_rm.meraki_organization_branding_policies:
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

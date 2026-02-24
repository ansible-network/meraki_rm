#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_auth_users.py for the implementation.

DOCUMENTATION = r'''
module: meraki_auth_users

short_description: Manage Meraki dashboard authentication users

description:
  - Manage Meraki dashboard authentication users for a network.
  - Supports merged, replaced, deleted, and gathered states.

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
    description: List of Meraki auth user configurations.
    type: list
    elements: dict
    suboptions:
      meraki_auth_user_id:
        description: Meraki auth user ID. Required for merged, replaced, deleted.
        type: str

      name:
        description: Name of the user.
        type: str

      email:
        description: Email address of the user.
        type: str

      password:
        description: Password for the user account.
        type: str

      account_type:
        description: Authorization type for user.
        type: str

      authorizations:
        description: User authorization info.
        type: list
        elements: dict

      is_admin:
        description: Whether the user is a Dashboard administrator.
        type: bool

      email_password_to_user:
        description: Whether Meraki should email the password to user.
        type: bool
'''

EXAMPLES = r'''
---
# Manage Meraki dashboard authentication users — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      meraki_auth_user_id: example
      name: Test-Config
      email: "admin@example.com"
      password: example
      account_type: example
      is_admin: true
      email_password_to_user: true

- name: Create auth_users with merged state
  cisco.meraki_rm.meraki_auth_users:
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

# Manage Meraki dashboard authentication users — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      meraki_auth_user_id: example
      name: Replaced-Config
      email: "replaced-admin@example.com"
      password: example
      account_type: example
      is_admin: true
      email_password_to_user: true

- name: Replace auth_users configuration
  cisco.meraki_rm.meraki_auth_users:
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

# Manage Meraki dashboard authentication users — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      meraki_auth_user_id: example
      name: Replaced-Config
      email: "replaced-admin@example.com"
      password: example
      account_type: example
      is_admin: true
      email_password_to_user: true

- name: Override all auth_users — desired state only
  cisco.meraki_rm.meraki_auth_users:
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

- name: Compare expected paths to result (subset: expected contained in result)
  ansible.builtin.set_fact:
    path_check: "{{ expected_paths | path_contained_in(result_paths) }}"
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

# Manage Meraki dashboard authentication users — gather current configuration

- name: Gather current auth_users configuration
  cisco.meraki_rm.meraki_auth_users:
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

# Manage Meraki dashboard authentication users — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      meraki_auth_user_id: example

- name: Delete auth_users configuration
  cisco.meraki_rm.meraki_auth_users:
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

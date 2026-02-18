#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_admins.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_admins

short_description: Manage Meraki organization administrators

description:
  - Manage Meraki organization administrators.
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
    description: List of admin configurations.
    type: list
    elements: dict
    suboptions:
      admin_id:
        description: Admin ID (for update/delete).
        type: str

      name:
        description: Admin name.
        type: str

      email:
        description: Admin email.
        type: str

      org_access:
        description: Admin's level of access to the organization.
        type: str
        choices:
          - full
          - read-only
          - enterprise
          - none

      tags:
        description: List of tag-based access controls.
        type: list
        elements: dict
        suboptions:
          tag:
            type: str
          access:
            type: str

      networks:
        description: List of network-based access controls.
        type: list
        elements: dict
        suboptions:
          id:
            type: str
          access:
            type: str

      authentication_method:
        description: Admin's authentication method.
        type: str
        choices:
          - Email
          - Cisco SecureX Sign-On

      account_status:
        description: Status of the admin's account.
        type: str

      two_factor_auth_enabled:
        description: Indicates whether two-factor authentication is enabled.
        type: bool

      has_api_key:
        description: Indicates whether the admin has an API key.
        type: bool

      last_active:
        description: Time when the admin was last active.
        type: str
'''

EXAMPLES = r'''
---
# Manage Meraki organization administrators — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      admin_id: example
      name: Test-Config
      email: "admin@example.com"
      org_access: full
      tags:
        - ansible
        - test
      authentication_method: Email
      account_status: example
      two_factor_auth_enabled: true

- name: Create organization_admins with merged state
  cisco.meraki_rm.meraki_organization_admins:
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

# Manage Meraki organization administrators — gather current configuration

- name: Gather current organization_admins configuration
  cisco.meraki_rm.meraki_organization_admins:
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

# Manage Meraki organization administrators — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      admin_id: example

- name: Delete organization_admins configuration
  cisco.meraki_rm.meraki_organization_admins:
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

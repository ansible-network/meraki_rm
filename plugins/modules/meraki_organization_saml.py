#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_saml.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_saml

short_description: Manage Meraki organization SAML settings

description:
  - Manage Meraki organization SAML SSO settings (singleton per organization).
  - GET/PUT /organizations/{organizationId}/saml
  - Supports merged, replaced, and gathered states.

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
      - gathered
    default: merged

  config:
    description: SAML settings configuration (singleton).
    type: list
    elements: dict
    suboptions:
      enabled:
        description: Whether SAML SSO is enabled.
        type: bool

      consumer_url:
        description: URL consuming SAML Identity Provider (IdP).
        type: str

      slo_logout_url:
        description: URL for redirect on sign out.
        type: str

      sso_login_url:
        description: URL for redirect to log in again when session expires.
        type: str

      x509cert_sha1_fingerprint:
        description: SHA1 fingerprint of the SAML certificate from IdP.
        type: str

      vision_consumer_url:
        description: URL consuming SAML IdP for Meraki Vision Portal.
        type: str

      sp_initiated:
        description: SP-Initiated SSO settings.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki organization SAML settings — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: true
      consumer_url: example
      slo_logout_url: example
      sso_login_url: example
      x509cert_sha1_fingerprint: example
      vision_consumer_url: example

- name: Create organization_saml with merged state
  cisco.meraki_rm.meraki_organization_saml:
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

# Manage Meraki organization SAML settings — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      enabled: false
      consumer_url: example
      slo_logout_url: example
      sso_login_url: example
      x509cert_sha1_fingerprint: example
      vision_consumer_url: example

- name: Replace organization_saml configuration
  cisco.meraki_rm.meraki_organization_saml:
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

# Manage Meraki organization SAML settings — gather current configuration

- name: Gather current organization_saml configuration
  cisco.meraki_rm.meraki_organization_saml:
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
'''

RETURN = r'''
config:
  description: The resulting resource configuration.
  type: list
  returned: always
'''

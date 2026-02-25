#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_organization_vpn.py for the implementation.

DOCUMENTATION = r'''
module: meraki_organization_vpn

short_description: Manage Meraki organization third-party VPN peers

description:
  - Manage Meraki organization third-party VPN peers (singleton).
  - GET/PUT /organizations/{organizationId}/appliance/vpn/thirdPartyVPNPeers
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
    description: Third-party VPN peers configuration (singleton).
    type: list
    elements: dict
    suboptions:
      peers:
        description: List of third-party VPN peers.
        type: list
        elements: dict
        suboptions:
          name:
            description: Peer identifier.
            type: str
          public_ip:
            description: Public IP address of the peer.
            type: str
          public_hostname:
            description: Hostname of the peer.
            type: str
          private_subnets:
            description: Remote subnets accessible through the VPN.
            type: list
            elements: str
          secret:
            description: Shared secret for IPsec authentication.
            type: str
          local_id:
            description: Local identification string.
            type: str
          remote_id:
            description: Remote identification string.
            type: str
          ike_version:
            description: IKE protocol version (1 or 2).
            type: str
          network_tags:
            description: Tags for network organization.
            type: list
            elements: str
'''

EXAMPLES = r'''
---
# Manage Meraki organization third-party VPN peers — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Create organization_vpn with merged state
  cisco.meraki_rm.meraki_organization_vpn:
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

# Manage Meraki organization third-party VPN peers — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:

- name: Replace organization_vpn configuration
  cisco.meraki_rm.meraki_organization_vpn:
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

# Manage Meraki organization third-party VPN peers — gather current configuration

- name: Gather current organization_vpn configuration
  cisco.meraki_rm.meraki_organization_vpn:
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

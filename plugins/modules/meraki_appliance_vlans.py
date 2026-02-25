#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_appliance_vlans.py for the implementation.

DOCUMENTATION = r'''
module: meraki_appliance_vlans

short_description: Manage Meraki appliance VLANs

description:
  - Manage Meraki appliance VLANs for a network.
  - Supports merged, replaced, deleted, and gathered states.

notes:
  - "Canonical key: C(vlan_id) — user-assigned, used for both identification and API routing."

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
    description: List of VLAN configurations.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description: VLAN ID (1-4094). Required for merged and deleted.
        type: str

      name:
        description: VLAN name.
        type: str

      subnet:
        description: Subnet (e.g., '192.168.1.0/24').
        type: str

      appliance_ip:
        description: Appliance IP on the VLAN.
        type: str

      group_policy_id:
        description: Group policy ID.
        type: str

      template_vlan_type:
        description: Type of subnetting for template networks.
        type: str
        choices:
          - same
          - unique

      cidr:
        description: CIDR for template networks.
        type: str

      mask:
        description: Mask for template networks.
        type: int

      dhcp_handling:
        description: How the appliance handles DHCP requests on this VLAN.
        type: str
        choices:
          - do_not_respond
          - relay
          - run_server

      dhcp_relay_server_ips:
        description: IPs of DHCP servers to relay requests to.
        type: list
        elements: str

      dhcp_lease_time:
        description: DHCP lease term.
        type: str
        choices:
          - 30_minutes
          - 1_hour
          - 4_hours
          - 12_hours
          - 1_day
          - 1_week

      dhcp_boot_options_enabled:
        description: Use DHCP boot options.
        type: bool

      dhcp_boot_next_server:
        description: DHCP boot next server.
        type: str

      dhcp_boot_filename:
        description: DHCP boot filename.
        type: str

      dhcp_options:
        description: DHCP options for responses.
        type: list
        elements: dict

      dns_nameservers:
        description: DNS nameservers for DHCP responses.
        type: str

      reserved_ip_ranges:
        description: Reserved IP ranges on the VLAN.
        type: list
        elements: dict
        suboptions:
          start:
            type: str
          end:
            type: str
          comment:
            type: str

      fixed_ip_assignments:
        description: Fixed IP assignments.
        type: dict

      ipv6:
        description: IPv6 configuration.
        type: dict

      mandatory_dhcp:
        description: Mandatory DHCP configuration.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki appliance VLANs — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      vlan_id: "100"
      name: Test-Config
      subnet: 192.168.128.0/24
      appliance_ip: 192.168.128.1
      group_policy_id: example
      template_vlan_type: same
      cidr: 192.168.128.0/24
      mask: 24

- name: Create appliance_vlans with merged state
  cisco.meraki_rm.meraki_appliance_vlans:
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

# Manage Meraki appliance VLANs — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      vlan_id: "100"
      name: Replaced-Config
      subnet: 10.20.0.0/24
      appliance_ip: 10.20.0.1
      group_policy_id: example
      template_vlan_type: unique
      cidr: 192.168.128.0/24
      mask: 24

- name: Replace appliance_vlans configuration
  cisco.meraki_rm.meraki_appliance_vlans:
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

# Manage Meraki appliance VLANs — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      vlan_id: "100"
      name: Replaced-Config
      subnet: 10.20.0.0/24
      appliance_ip: 10.20.0.1
      group_policy_id: example
      template_vlan_type: unique
      cidr: 192.168.128.0/24
      mask: 24

- name: Override all appliance_vlans — desired state only
  cisco.meraki_rm.meraki_appliance_vlans:
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

# Manage Meraki appliance VLANs — gather current configuration

- name: Gather current appliance_vlans configuration
  cisco.meraki_rm.meraki_appliance_vlans:
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

# Manage Meraki appliance VLANs — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      vlan_id: "100"

- name: Delete appliance_vlans configuration
  cisco.meraki_rm.meraki_appliance_vlans:
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
before:
  description: Resource configuration before the run.
  type: list
  returned: when state is merged, replaced, overridden, or deleted
  elements: dict

after:
  description: Resource configuration after the run.
  type: list
  returned: when state is merged, replaced, overridden, or deleted
  elements: dict

gathered:
  description: Current resource configuration (read-only).
  type: list
  returned: when state is gathered
  elements: dict

config:
  description: Alias for C(after) (or C(gathered) when state=gathered).
  type: list
  returned: always
  elements: dict
'''

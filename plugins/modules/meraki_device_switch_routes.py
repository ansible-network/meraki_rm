#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_device_switch_routes.py for the implementation.

DOCUMENTATION = r'''
module: meraki_device_switch_routes

short_description: Manage Meraki device switch routing interfaces

description:
  - Manage Meraki device switch routing interfaces (L3 interfaces).
  - Scope is device serial. Supports merged, replaced, deleted, and gathered states.

version_added: "0.1.0"

author:
  - Cisco Meraki

options:
  serial:
    description: Device serial number.
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
    description: List of switch routing interface configurations.
    type: list
    elements: dict
    suboptions:
      interface_id:
        description: Interface ID. Required for merged, replaced, deleted.
        type: str

      name:
        description: Interface name.
        type: str

      subnet:
        description: IPv4 subnet.
        type: str

      interface_ip:
        description: IPv4 address.
        type: str

      default_gateway:
        description: IPv4 default gateway.
        type: str

      vlan_id:
        description: VLAN ID.
        type: int

      multicast_routing:
        description: Multicast routing status.
        type: str

      ospf_settings:
        description: IPv4 OSPF settings.
        type: dict

      dhcp_mode:
        description: DHCP mode for the interface.
        type: str

      dhcp_relay_server_ips:
        description: DHCP relay server IPs.
        type: list
        elements: str
'''

EXAMPLES = r'''
---
# Manage Meraki device switch routing interfaces — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      interface_id: example
      name: Test-Config
      subnet: 192.168.128.0/24
      interface_ip: 10.0.0.1
      default_gateway: 10.0.0.1
      vlan_id: "100"
      multicast_routing: example
      dhcp_mode: example

- name: Create device_switch_routes with merged state
  cisco.meraki_rm.meraki_device_switch_routes:
    serial: "Q2XX-XXXX-XXXX"
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

# Manage Meraki device switch routing interfaces — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      interface_id: example
      name: Replaced-Config
      subnet: 10.20.0.0/24
      interface_ip: 10.0.0.1
      default_gateway: 10.0.0.1
      vlan_id: "100"
      multicast_routing: example
      dhcp_mode: example

- name: Replace device_switch_routes configuration
  cisco.meraki_rm.meraki_device_switch_routes:
    serial: "Q2XX-XXXX-XXXX"
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

# Manage Meraki device switch routing interfaces — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      interface_id: example
      name: Replaced-Config
      subnet: 10.20.0.0/24
      interface_ip: 10.0.0.1
      default_gateway: 10.0.0.1
      vlan_id: "100"
      multicast_routing: example
      dhcp_mode: example

- name: Override all device_switch_routes — desired state only
  cisco.meraki_rm.meraki_device_switch_routes:
    serial: "Q2XX-XXXX-XXXX"
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

# Manage Meraki device switch routing interfaces — gather current configuration

- name: Gather current device_switch_routes configuration
  cisco.meraki_rm.meraki_device_switch_routes:
    serial: "Q2XX-XXXX-XXXX"
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

# Manage Meraki device switch routing interfaces — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      interface_id: example
      vlan_id: "100"

- name: Delete device_switch_routes configuration
  cisco.meraki_rm.meraki_device_switch_routes:
    serial: "Q2XX-XXXX-XXXX"
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

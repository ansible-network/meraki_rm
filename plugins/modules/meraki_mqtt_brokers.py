#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_mqtt_brokers.py for the implementation.

DOCUMENTATION = r'''
module: meraki_mqtt_brokers

short_description: Manage Meraki MQTT brokers

description:
  - Manage Meraki MQTT brokers for a network.
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
    description: List of MQTT broker configurations.
    type: list
    elements: dict
    suboptions:
      mqtt_broker_id:
        description: MQTT broker ID. Required for merged, replaced, deleted.
        type: str

      name:
        description: Name of the MQTT broker.
        type: str

      host:
        description: Host name or IP address of the MQTT broker.
        type: str

      port:
        description: Port for the MQTT broker.
        type: int

      authentication:
        description: Authentication settings.
        type: dict

      security:
        description: Security settings.
        type: dict
'''

EXAMPLES = r'''
---
# Manage Meraki MQTT brokers — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      mqtt_broker_id: example
      name: Test-Config
      host: mqtt.example.com
      port: 1883

- name: Create mqtt_brokers with merged state
  cisco.meraki_rm.meraki_mqtt_brokers:
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

# Manage Meraki MQTT brokers — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      mqtt_broker_id: example
      name: Replaced-Config
      host: mqtt.example.com
      port: 1883

- name: Replace mqtt_brokers configuration
  cisco.meraki_rm.meraki_mqtt_brokers:
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

# Manage Meraki MQTT brokers — override all instances
# Ensures ONLY these resources exist; any not listed are deleted.

- name: Define desired-state configuration
  ansible.builtin.set_fact:
    expected_config:
      mqtt_broker_id: example
      name: Replaced-Config
      host: mqtt.example.com
      port: 1883

- name: Override all mqtt_brokers — desired state only
  cisco.meraki_rm.meraki_mqtt_brokers:
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

# Manage Meraki MQTT brokers — gather current configuration

- name: Gather current mqtt_brokers configuration
  cisco.meraki_rm.meraki_mqtt_brokers:
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

# Manage Meraki MQTT brokers — remove configuration

- name: Define resource to delete
  ansible.builtin.set_fact:
    expected_config:
      mqtt_broker_id: example

- name: Delete mqtt_brokers configuration
  cisco.meraki_rm.meraki_mqtt_brokers:
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

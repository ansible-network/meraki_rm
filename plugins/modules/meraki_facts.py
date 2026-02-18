#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_facts.py for the implementation.

DOCUMENTATION = r'''
module: meraki_facts

short_description: Gather facts about Meraki Dashboard resources

description:
  - Gather facts about organizations, networks, devices, and inventory
    from the Meraki Dashboard API.
  - This is a gather-only module that collects information without
    making changes.

version_added: "0.1.0"

author:
  - Cisco Meraki

options:
  gather_subset:
    description: What to gather.
    type: list
    elements: str
    default: [all]
    choices:
      - all
      - organizations
      - networks
      - devices
      - inventory

  organization_id:
    description: Scope to a specific organization.
    type: str

  network_id:
    description: Scope to a specific network.
    type: str
'''

EXAMPLES = r'''
---
# Gather all Meraki facts

- name: Gather all Meraki facts
  cisco.meraki_rm.meraki_facts:
    organization_id: "N_123456789012345678"
    gather_subset:
      - all
  register: all_facts

- name: Display gathered facts
  ansible.builtin.debug:
    var: all_facts

- name: Gather only organization info
  cisco.meraki_rm.meraki_facts:
    organization_id: "N_123456789012345678"
    gather_subset:
      - organizations

- name: Gather networks for a specific org
  cisco.meraki_rm.meraki_facts:
    organization_id: "N_123456789012345678"
    gather_subset:
      - networks
'''

RETURN = r'''
ansible_facts:
  description: Gathered facts about Meraki resources.
  type: dict
  returned: always
'''

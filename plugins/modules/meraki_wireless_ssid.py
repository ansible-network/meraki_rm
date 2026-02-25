#!/usr/bin/python
# -*- coding: utf-8 -*-

# This module is implemented as an action plugin.
# See plugins/action/meraki_wireless_ssid.py for the implementation.

DOCUMENTATION = r'''
module: meraki_wireless_ssid

short_description: Manage Meraki wireless SSIDs

description:
  - Manage wireless SSIDs for a Meraki network.
  - SSIDs are numbered 0-14 and always exist; no create or delete.
  - Supports merged, replaced, and gathered states.

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
      - gathered
    default: merged

  config:
    description: List of SSID configurations.
    type: list
    elements: dict
    suboptions:
      number:
        description: SSID number (0-14). Required for merged and replaced.
        type: int
        required: true

      name:
        description: SSID name.
        type: str

      enabled:
        description: Whether the SSID is enabled.
        type: bool

      auth_mode:
        description: Authentication mode.
        type: str
        choices:
          - open
          - psk
          - 8021x-meraki
          - 8021x-radius
          - ipsk-with-radius
          - ipsk-without-radius

      encryption_mode:
        description: Encryption mode for the SSID.
        type: str

      psk:
        description: Pre-shared key (for PSK auth). Write-only; not returned by API.
        type: str

      wpa_encryption_mode:
        description: WPA encryption mode.
        type: str
        choices:
          - WPA1 and WPA2
          - WPA2 only
          - WPA3 Transition Mode
          - WPA3 only

      ip_assignment_mode:
        description: Client IP assignment mode.
        type: str
        choices:
          - NAT mode
          - Bridge mode
          - Layer 3 roaming
          - Layer 3 roaming with a concentrator
          - VPN

      use_vlan_tagging:
        description: Whether to use VLAN tagging.
        type: bool

      default_vlan_id:
        description: Default VLAN ID for all other APs.
        type: int

      vlan_id:
        description: VLAN ID for VLAN tagging.
        type: int

      splash_page:
        description: Splash page type.
        type: str
        choices:
          - None
          - Click-through splash page
          - Billing
          - Password-protected with Meraki RADIUS
          - Password-protected with custom RADIUS
          - Password-protected with Active Directory
          - Password-protected with LDAP
          - SMS authentication
          - Systems Manager Sentry
          - Facebook Wi-Fi
          - Google OAuth
          - Sponsored guest

      band_selection:
        description: Band selection for the SSID.
        type: str
        choices:
          - DSSS
          - FHSS
          - 802.11a
          - 802.11b/g
          - 802.11g only
          - 802.11a/n
          - 802.11g/n
          - 802.11b/g/n
          - 802.11a/n/ac
          - 802.11a/n/ac/ax (Wi-Fi 6)
          - 802.11b/g/n/ax (Wi-Fi 6)

      min_bitrate:
        description: Minimum bitrate in Mbps.
        type: float

      per_client_bandwidth_limit_up:
        description: Per-client upload bandwidth limit in Kbps (0 = no limit).
        type: int

      per_client_bandwidth_limit_down:
        description: Per-client download bandwidth limit in Kbps (0 = no limit).
        type: int

      per_ssid_bandwidth_limit_up:
        description: Per-SSID upload bandwidth limit in Kbps (0 = no limit).
        type: int

      per_ssid_bandwidth_limit_down:
        description: Per-SSID download bandwidth limit in Kbps (0 = no limit).
        type: int

      visible:
        description: Whether the SSID is advertised (visible) or hidden.
        type: bool

      available_on_all_aps:
        description: Whether the SSID is broadcast on all APs.
        type: bool

      availability_tags:
        description: AP tags for SSID availability (when available_on_all_aps is false).
        type: list
        elements: str
'''

EXAMPLES = r'''
---
# Manage Meraki wireless SSIDs — create or update

- name: Define expected configuration
  ansible.builtin.set_fact:
    expected_config:
      number: 1
      name: Test-Config
      enabled: true
      auth_mode: open
      encryption_mode: wpa
      psk: testpassword123
      wpa_encryption_mode: WPA1 and WPA2
      ip_assignment_mode: NAT mode

- name: Create wireless_ssid with merged state
  cisco.meraki_rm.meraki_wireless_ssid:
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

# Manage Meraki wireless SSIDs — full resource replacement

- name: Define replacement configuration
  ansible.builtin.set_fact:
    expected_config:
      number: 1
      name: Replaced-Config
      enabled: false
      auth_mode: psk
      encryption_mode: wpa
      psk: testpassword123
      wpa_encryption_mode: WPA2 only
      ip_assignment_mode: Bridge mode

- name: Replace wireless_ssid configuration
  cisco.meraki_rm.meraki_wireless_ssid:
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

# Manage Meraki wireless SSIDs — gather current configuration

- name: Gather current wireless_ssid configuration
  cisco.meraki_rm.meraki_wireless_ssid:
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
'''

RETURN = r'''
config:
  description: The resulting resource configuration.
  type: list
  returned: always
'''

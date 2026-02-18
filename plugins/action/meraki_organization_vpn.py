"""Action plugin for meraki_organization_vpn module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'org_vpn'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.org_vpn.UserOrgVpn'
    SUPPORTS_DELETE = False

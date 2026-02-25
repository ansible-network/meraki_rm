"""Action plugin for meraki_organization_alert_profiles module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.org_alert_profile.UserOrgAlertProfile'

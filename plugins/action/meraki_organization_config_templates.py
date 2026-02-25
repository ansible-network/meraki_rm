"""Action plugin for meraki_organization_config_templates module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.config_template.UserConfigTemplate'

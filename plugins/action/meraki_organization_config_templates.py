"""Action plugin for meraki_organization_config_templates module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'config_template'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.config_template.UserConfigTemplate'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'config_template_id'

"""Action plugin for meraki_organization_admins module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'admin'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.admin.UserAdmin'
    PRIMARY_KEY = 'admin_id'

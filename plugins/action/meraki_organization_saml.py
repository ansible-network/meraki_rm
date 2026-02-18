"""Action plugin for meraki_organization_saml module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'saml'
    SCOPE_PARAM = 'organization_id'
    USER_MODEL = 'plugins.plugin_utils.user_models.saml.UserSaml'
    SUPPORTS_DELETE = False

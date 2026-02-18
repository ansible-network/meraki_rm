"""Action plugin for meraki_device module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'device'
    SCOPE_PARAM = 'serial'
    USER_MODEL = 'plugins.plugin_utils.user_models.device.UserDevice'
    SUPPORTS_DELETE = False

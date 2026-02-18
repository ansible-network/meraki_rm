"""Action plugin for meraki_device_management_interface module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'device_management_interface'
    SCOPE_PARAM = 'serial'
    USER_MODEL = 'plugins.plugin_utils.user_models.device_management_interface.UserDeviceManagementInterface'
    SUPPORTS_DELETE = False

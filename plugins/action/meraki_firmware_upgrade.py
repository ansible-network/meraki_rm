"""Action plugin for meraki_firmware_upgrade module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.firmware_upgrade.UserFirmwareUpgrade'

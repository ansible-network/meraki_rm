"""Action plugin for meraki_wireless_air_marshal_rules module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.air_marshal.UserAirMarshal'

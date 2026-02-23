"""Action plugin for meraki_wireless_air_marshal_rules module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'air_marshal'
    USER_MODEL = 'plugins.plugin_utils.user_models.air_marshal.UserAirMarshal'
    PRIMARY_KEY = 'rule_id'
    # No network-level GET — listing is at org level only
    VALID_STATES = frozenset({'merged', 'replaced', 'deleted'})

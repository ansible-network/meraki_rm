"""Action plugin for meraki_switch_link_aggregations module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_link_aggregation'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_link_aggregation.UserSwitchLinkAggregation'
    SYSTEM_KEY = 'link_aggregation_id'

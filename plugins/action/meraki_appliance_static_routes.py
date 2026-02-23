"""Action plugin for meraki_appliance_static_routes module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'static_route'
    USER_MODEL = 'plugins.plugin_utils.user_models.static_route.UserStaticRoute'
    PRIMARY_KEY = 'static_route_id'

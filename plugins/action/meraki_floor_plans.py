"""Action plugin for meraki_floor_plans module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.floor_plan.UserFloorPlan'

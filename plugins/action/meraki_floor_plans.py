"""Action plugin for meraki_floor_plans module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'floor_plan'
    USER_MODEL = 'plugins.plugin_utils.user_models.floor_plan.UserFloorPlan'
    CANONICAL_KEY = 'name'
    SYSTEM_KEY = 'floor_plan_id'

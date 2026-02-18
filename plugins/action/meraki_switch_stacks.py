"""Action plugin for meraki_switch_stacks module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'switch_stack'
    USER_MODEL = 'plugins.plugin_utils.user_models.switch_stack.UserSwitchStack'
    PRIMARY_KEY = 'switch_stack_id'
    # Spec only has POST (create) and DELETE — no PUT for update
    VALID_STATES = frozenset({'merged', 'deleted', 'gathered'})

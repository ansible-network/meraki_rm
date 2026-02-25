"""Action plugin for meraki_mqtt_brokers module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    USER_MODEL = 'plugins.plugin_utils.user_models.mqtt_broker.UserMqttBroker'

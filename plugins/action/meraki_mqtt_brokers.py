"""Action plugin for meraki_mqtt_brokers module."""

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'mqtt_broker'
    USER_MODEL = 'plugins.plugin_utils.user_models.mqtt_broker.UserMqttBroker'
    PRIMARY_KEY = 'mqtt_broker_id'

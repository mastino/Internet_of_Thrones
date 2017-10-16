import paho.mqtt.client as paho
from functools import partial

class MQTTClient:

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        pass

    @staticmethod
    def on_disconnect(client, userdata, rc):
        pass

    @staticmethod
    def on_log(client, userdata, level, buf):
        pass

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        pass

    @staticmethod
    def get_will_topic():
        return "cis650/Internet_of_Thrones/null"

    @staticmethod
    def get_will():
        return ":("

    def __init__(self):
        # Instantiate the MQTT client
        self.mqtt_client = paho.Client()

        # set up handlers
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = partial(self.on_message, mqtt_client = self)
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log = self.on_log
        self.mqtt_client.will_set(self.get_will_topic(), self.get_will(), 0, False)

        # set the broker and connect
        broker = 'sansa.cs.uoregon.edu'  # Boyana's server
        self.mqtt_client.connect(broker, '1883')
        self.mqtt_client.loop_start()  # start the network loop

    def publish(self, topic, message):
        self.mqtt_client.publish('cis650/Internet_of_Thrones/' + topic, message)

    def subscribe(self, topic):
        self.mqtt_client.subscribe('cis650/Internet_of_Thrones/' + topic)

    def disconnect(self):
        self.mqtt_client.disconnect()

    def loop_stop(self):
        self.mqtt_client.loop_stop()

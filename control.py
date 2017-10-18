import time, socket, sys
from datetime import datetime as dt
import paho.mqtt.client as paho
import signal
from mqtt_client import MQTTClient

class Control(MQTTClient):
    """docstring for Control"""
    def __init__(self, cap = 3):
        super(self.__class__, self).__init__()
        self.platform = 0
        self.CAP = cap
        self.subscribe("turnstile")
        self.subscribe("car")
        self.subscribe("bcast")
        self.publish('turnstile', "empty")


    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
        print msg.topic, msg.payload
        if msg.topic == "turnstile" and msg.payload == "incoming!":
            self.handle_passnger()

        elif msg.topic == "car":
            m,i = msg.payload.split(":")
            if m == "available" and self.platform >= self.CAP:
                self.confirm_car(i)

        elif msg.topic == "bcast":
            if msg.payload == "quit":
                self.disconnect()
                self.loop_stop()

    def handle_passnger(self):
        self.platform += 1
        if self.platform >= self.CAP:
            self.publish('turnstile', "full")
            self.request_car()

    def request_car(self):
        self.publish('car', "request")

    def confirm_car(self, car):
        msg = "pickup:" + car
        self.publish('car', msg)
        self.publish('turnstile', "empty")
        self.platform -= CAP

        

c = Control()
while(True):
    pass




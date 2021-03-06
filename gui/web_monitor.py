from flask import Flask, Response, render_template, url_for, request, redirect, jsonify
import logging, time, Queue, copy
import atexit
from mqtt_client import MQTTClient

app = Flask(__name__)
app.secret_key = 'lol'
app.debug = True
app.logger.setLevel(logging.DEBUG)

waiting_to_display = []
last_ten_messages = Queue.Queue()
property1_dump = []
property2_dump = []

def add_to_last_ten(msg):
    global last_ten_messages
    if last_ten_messages.qsize() >= 10:
        last_ten_messages.get()
    last_ten_messages.put(msg)

class Monitor(MQTTClient):

    phil0_arise   = False
    phil0_sitdown = False
    phil1_arise   = True

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
    	waiting_to_display.append( "[[%s]] %s" % (msg.topic, msg.payload) )
        add_to_last_ten( "[[%s]] %s" % (msg.topic, msg.payload) )
        mqtt_client.assert1(msg.topic.split('/')[-1], msg.payload)
        mqtt_client.assert2(msg.topic.split('/')[-1], msg.payload)

    def assert1(self, topic, msg):
        if topic == 'butler':
            action, phil_id = msg.split(':')
            if action == 'eating' and phil_id == '0' and not self.phil0_arise:
                temp = copy.copy(last_ten_messages)
                while not temp.empty():
                    property1_dump.append(temp.get())
            elif action == 'arise' and phil_id == '0':
                self.phil0_arise = True

    def assert2(self, topic, msg):
        if topic == 'butler':
            action, phil_id = msg.split(':')
            if action == 'sit' and phil_id == '0' and not self.phil0_sitdown:
                self.phil1_arise = False
                self.phil0_sitdown = True
            elif action == 'arise' and phil_id == '1' and self.phil0_sitdown:
                self.phil1_arise = True
                self.phil0_sitdown = False
            elif action == 'arise' and phil_id == '1' and not self.phil0_sitdown:
                temp = copy.copy(last_ten_messages)
                while not temp.empty():
                    property2_dump.append(temp.get())
            elif action == 'sit' and phil_id == '0' and not self.phil1_arise:
                temp = copy.copy(last_ten_messages)
                while not temp.empty():
                    property2_dump.append(temp.get())

def monitor_cleanup(client):
    client.disconnect()
    client.loop_stop()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/_msgs")
def msgs():
    global waiting_to_display
    global property1_dump
    global property2_dump
    if property1_dump:
        res = jsonify(msgs=waiting_to_display, property1=property1_dump)
        property1_dump = []
    elif property2_dump:
        res = jsonify(msg=waiting_to_display, property2=property2_dump)
        property2_dump = []
    else:
        res = jsonify(msgs=waiting_to_display)
    waiting_to_display = []
    return res

if __name__ == "__main__":
    monitor = Monitor()
    atexit.register(monitor_cleanup, monitor)
    monitor.subscribe('#')
    app.run(host='localhost', port=5000, threaded=True)

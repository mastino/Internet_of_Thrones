from flask import Flask, Response, render_template, url_for, request, redirect, jsonify
import logging, time
import atexit
from mqtt_client import MQTTClient

app = Flask(__name__)
app.secret_key = 'lol'
app.debug = True
app.logger.setLevel(logging.DEBUG)

waiting_to_display = []

class Monitor(MQTTClient):

    @staticmethod
    def on_message(client, userdata, msg, mqtt_client):
    	waiting_to_display.append( "[[%s]] %s" % (msg.topic, msg.payload) )

def monitor_cleanup(client):
    client.disconnect()
    client.loop_stop()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/_msgs")
def msgs():
    global waiting_to_display
    dump = waiting_to_display[:]
    waiting_to_display = []
    return jsonify(msgs=dump)

if __name__ == "__main__":
    monitor = Monitor()
    atexit.register(monitor_cleanup, monitor)
    monitor.subscribe('#')
    app.run(host='localhost', port=5000, threaded=True)

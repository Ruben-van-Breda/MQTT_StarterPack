import threading
from flask import Flask, jsonify, render_template, request, redirect, url_for

from datetime import datetime
from flask_cors import CORS


import sys
import os
import time

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to get the `web_client` directory (since your script is inside `common/tests`)
web_client_directory = os.path.abspath(os.path.join(current_directory, '..'))

# Append to sys.path
sys.path.append(web_client_directory)

from lib.MQTT_Standard import MQTTStandard
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


global mqtt_client
global connection_status

connection_status = "Unknown"
connection_status_backgroud_thread = None
stop_thread_event = threading.Event()  # event object to signal the thread to stop

messages = []
defined_publish_calls = []


@app.route('/', methods=['GET', 'POST'])
def index():
    global connection_status,  connection_status_backgroud_thread
    print("Checking background thread")
    return render_template('index.html', connection_status=connection_status)

def on_message_received(client, userdata, msg):
    print("\nServer Message received:\n\ttopic: " + msg.topic + "\n\tPayload: " + str(msg.payload.decode("utf-8")))

    message = {
            'text': msg.payload.decode("utf-8"),
            'topic': msg.topic,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    messages.append(message)
    socketio.emit('new_message', message)



@app.route("/connect", methods=['POST'])
def connect():
    global mqtt_client, connection_status_backgroud_thread

    # get variables from json arguments
    data = request.get_json()  # Get JSON data from the request
    broker = data.get('broker')
    port = data.get('port')
    username = data.get('username')
    password = data.get('password')

    print(broker, port, username, password)

    try:
        mqtt_client = MQTTStandard(broker_server=broker, broker_port=int(port), broker_username=username, broker_password=password,
                                    sub_topic="all/#", pub_topic="all/test" , on_message=on_message_received )
        mqtt_client.connect()

        # Start background thread to check connection to broker
        # Reset the event for a new connection status checker thread
        # stop_thread_event.clear()
        # connection_status_backgroud_thread = socketio.start_background_task(target=check_connection_status)

        socketio.emit('badge', "Connected Successfully")
        
    except Exception as e:
        print("Error connecting to broker", e)
        return jsonify(status="error", message="Error connecting to broker"), 500

    return jsonify(status="success", message="Connected"), 200

@app.route("/publish", methods=['POST'])
def _publish_message():
    print("Publishing message")
    global mqtt_client
    data = request.get_json()
    topic = data.get('topic')
    message_text = data.get('message')
    message_text = message_text.encode("utf-8")



    try:
        message = {
            'text': message_text.decode("utf-8"),
            'topic': topic,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        messages.append(message)
        
        # publish message to MQTT broker
        mqtt_client.publish(topic, message_text.decode("utf-8"), qos=1)

    except Exception as e:
        print(f"Error publishing message: {e}")
        return jsonify(status="error", message="Error publishing message"), 500

    return jsonify(status="success", messages=messages), 200

def _publish_call(topic_name, message_text):

    global mqtt_client
    topic = topic_name
    message_text = message_text
    print(f"RUNNING CALL message: {message_text} to topic: {topic}")

    try:
        print(f"MQTT PUBLISHING: \n TOPIC: {topic} \n{message_text}")
        mqtt_client.publish(topic, message_text, qos=1)
    except Exception as e:
        print(f"Error publishing message: {e}")
        socketio.emit('badge', f"Error publishing message: {e}")
        return jsonify(status="error", message="Error publishing message"), 500

# check function to listen on socketio
@socketio.on('run_defined_call')
def run_defined_call(message):
    _publish_call(message.get("topic"), message.get("message"))
    

def check_connection_status():
    while True:
        # Replace with your actual logic to check connection
        is_connected = mqtt_client.is_connected()
        socketio.emit('update_connection_status', {'status': is_connected})
        time.sleep(10)  # Checking every 10 seconds


@app.route('/add_call', methods=['POST'])
def add_defined_pub_call():
    try:
        print("Adding defined publish call")
        print("ADD_CALL:::::::::::::::::::::::::::::")
        global defined_publish_calls
        try:
            data = request.form.get_json()
            print("DATA PASSED", data)

        except Exception as e:
            data = request.get_json()
            print("DATA FAILED", data)
            print(e)

        topic = data.get('topic')
        message = data.get('message')
        name = data.get('name')

        print("DATA:::::::: ", topic, message, name)
        new_item = {'topic': topic, 'message': message, 'name': name}
        defined_publish_calls.append(new_item)

        badge_msg =  f"Added new defined publish call: {topic} {message}, {name}"
        print(badge_msg)

        # UPDATE JS in HTML
        socketio.emit('update_defined_calls',new_item)
        return jsonify(status="success", message="Call added"), 200
    except Exception as e:
        print(f"Error adding defined publish call: {e}")
        return jsonify(status="error", message="Error adding defined publish call"), 500



if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
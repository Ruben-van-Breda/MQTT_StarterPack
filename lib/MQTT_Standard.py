import paho.mqtt.client as paho
from paho import mqtt

import json


class MQTTStandard():
    """
        MQTTStandard is a standard class for MQTT client and server communication.
    """

    def __init__(self, broker_server=None, broker_port=None, broker_username=None,
                 broker_password=None, sub_topic=None, pub_topic=None, config_file=None,
                 on_connect=None, on_publish=None, on_subscribe=None, on_message=None):
        if config_file:
            self.config = self.load_config(config_file)
        else:
            self.config = {
                "BROKER_SERVER": broker_server,
                "BROKER_PORT": broker_port,
                "BROKER_USERNAME": broker_username,
                "BROKER_PASSWORD": broker_password,
                "SUB_TOPIC": sub_topic,
                "PUB_TOPIC": pub_topic
            }
        self.client = None
        self.on_connect = on_connect
        self.on_publish = on_publish
        self.on_subscribe = on_subscribe
        self.on_message = on_message

        # Register the default on_subscribe callback
        
    def load_config(self, config_file):
        """
            Load configuration from a JSON file.
        """
        print("MQTTStandard loading configuration from file: " + config_file)
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                print(config)
            return config
        except FileNotFoundError:
            print("MQTTStandard loading configuration from file: " + config_file)
            raise FileNotFoundError("Configuration file not found")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in the configuration file")
    
     # setting callbacks for different events to see if it works, print the message etc.
    
    def on_connect_default(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    def on_publish_default(self, client, userdata, mid, properties=None):
        print("Defaul Publish Called: Broadcast received with code %s." % mid)
      
    def on_subscribe_default(client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message_default(client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    
    def publish(self, topic, msg, qos=1):
        """
            Publish a message to a topic.
        """
        print("Calling client.publish on topic " + topic + " data: " + str(msg)) 
        # bytes msg
        msg = msg.encode("utf-8")
        self.client.publish(topic, msg, qos=1)

    def connect(self) -> paho.Client:
        """
            Connect to the MQTT broker using the configuration.
            Returns a client object
        """

        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

        self.client.on_connect = self.on_connect if self.on_connect else self.on_connect_default
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # Set username and password 
        self.client.username_pw_set(self.config["BROKER_USERNAME"], self.config["BROKER_PASSWORD"])

        # Establish connection to the broker
        try:
            print("Connecting to broker: " + self.config["BROKER_SERVER"])
            print("Connecting port: " + str(self.config["BROKER_PORT"]))
            connection_status = self.client.connect(self.config["BROKER_SERVER"], self.config["BROKER_PORT"])
        except ConnectionRefusedError:
            print("Connection refused")
            raise ConnectionRefusedError("Connection refused")
        print("Connection status: %s" % connection_status)


        # self.client.on_subscribe = self.on_subscribe if self.on_subscribe else self.on_subscribe_default
        self.client.on_message = self.on_message if self.on_message else self.on_message_default
        self.client.on_publish = self.on_publish if self.on_publish else self.on_publish_default

        self.client.on_subscribe = self.on_subscribe

        # Subscribe to the topic specified in the configuration
        self.client.subscribe(self.config["SUB_TOPIC"], qos=1)
        # Publish a message to a topic specified in the configuration to indicate that the client is connected
        self.client.publish("all/test", "MQTT Client: connected", qos=1)

        # Start the loop to listen for messages
        self.start()

        return self.client

    def is_connected(self):
        print("Checking connection")
        return self.client.is_connected()

    def start(self):
        self.client.loop_start()

    def setup_depricated(self):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(self.config["BROKER_USERNAME"], self.config["BROKER_PASSWORD"])

        connection_status = self.client.connect(self.config["BROKER_SERVER"], self.config["BROKER_PORT"])
        print("Connection status: %s" % connection_status)

        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.client.subscribe(self.config["SUB_TOPIC"], qos=1)
        return self.client
import json
import time

import network
from machine import Pin
from umqtt.simple import MQTTClient


class MqttMicroprocessor:
    def __init__(
        self,
        config_file=None,
        broker_server=None,
        broker_port=8883,
        sub_topic=None,
        client_id=None,
        broker_username=None,
        broker_password=None,
        wifi_ssid=None,
        wifi_password=None,
        on_message=None,
        on_publish=None,
        built_in_led_pin="LED",
    ):
        if config_file:
            self.config = self.load_config(config_file)
        else:
            self.config = {
                "CLIENT_ID": client_id,
                "BROKER_SERVER": broker_server,
                "BROKER_PORT": broker_port,
                "BROKER_USERNAME": broker_username,
                "BROKER_PASSWORD": broker_password,
                "SUB_TOPIC": sub_topic,
                "WIFI_SSID": wifi_ssid,
                "WIFI_PASSWORD": wifi_password,
            }

        
        self.built_in_led = Pin(self.built_in_led, Pin.OUT)
        self.built_in_led.off()

        self.last_connection_check = None
        self.client = None
        self.ip_address = None

    @staticmethod
    def load_config(config_file):
        print("MQTTStandard loading configuration from file: " + config_file)
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                print(config)
            return config
        except json.JSONDecodeError as e:
            print("ERrored to read configuration from file: " + config_file)
            print(e)
        except Exception as e:
            print("MQTTStandard loading configuration from file: " + config_file)
            exit(-1)

    def set_sub_topic(self, topic):
        self.topic = topic
        return self.topic

    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.config["WIFI_SSID"], self.config["WIFI_PASSWORD"])
        while not wlan.isconnected():
            print("Waiting for WiFi connection...")
            time.sleep(1)
        print("Connected to WiFi!")
        self.ip_address = wlan.ifconfig()[0]
        print("IP address:", self.ip_address)
        self._indicate_connection_status()
        self.last_connection_check = time.time()

    def _indicate_connection_status(self):
        for _ in range(3):
            self.built_in_led.on()
            time.sleep_ms(10)
            self.built_in_led.off()
            time.sleep_ms(10)

    def connect(self, sub_topic, on_msg_func):
        self.connect_to_wifi()
        self.client = MQTTClient(
            self.config["CLIENT_ID"],
            self.config["BROKER_SERVER"],
            self.config["BROKER_PORT"],
            self.config["BROKER_USERNAME"],
            self.config["BROKER_PASSWORD"],
            ssl=True,
            ssl_params={"server_hostname": self.config["BROKER_SERVER"]},
        )
        self.client.set_callback(on_msg_func)

        try:
            self.client.connect()
            self.last_connection_check = time.time()
        except Exception as e:
            print("Error trying to connect to broker: %s" % e)
            exit(-1)

        self.built_in_led.value(1)
        try:
            # bytes
            sub_topic = self.config["SUB_TOPIC"].encode("utf-8")
            self.client.subscribe(sub_topic)
        except Exception as e:
            print("Error trying to subscribe to topic: %s" % e)
            exit(-1)

        print("Connected to", self.config["BROKER_SERVER"], "and subscribed to", self.config["SUB_TOPIC"])
        self.client.publish(self.config["PUB_TOPIC"], f"{self.config['CLIENT_ID']} Deivce Booted and Connected: IP {self.ip_address}")

        return self.client

    def set_on_message_callback(self, func):
        self.client.set_callback(func)
        return self.client

    def check_connection(self, client):
        now = time.time()
        if now - self.last_connection_check < 300:
            return True
        self._indicate_connection_status()
        self.last_connection_check = now
        try:
            self.client.ping()
            print("Connected to", self.config['BROKER_SERVER'], "and pinged the broker")
            self.client.publish(
                self.config["PUB_TOPIC"], f" {self.config['CLIENT_ID']} Deivce alive and connected: IP {self.ip_address}"
            )
            return True
        except Exception as e:
            print("Disconnected from broker. Reconnecting...")
            try:
                self.client.connect()
                self.client.subscribe(self.topic)
                print("Reconnected to", self.config['BROKER_SERVER'], "and subscribed to", self.config["SUB_TOPIC"])
                self.client.publish(self.config["PUB_TOPIC"], f"{self.config['CLIENT_ID']} Deivce Reconnected: IP {self.ip_address}")
                return True
            except Exception as e:
                print("Failed to reconnect:", e)
                self.built_in_led.value(0)
                return False

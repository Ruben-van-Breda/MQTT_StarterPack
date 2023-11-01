from mqtt_foudation.micropython.mqtt_microprocessor import MqttMicroprocessor
import time

# MQTT SETTINGS
SUB_TOPIC = b"all/esp32"

print("--------JAR Technologies------")

print("MQTT Client Created")

def on_message(topic, msg):
    print('Received message:', msg, 'on topic:', topic)
    msg = msg.decode("utf-8")

    if "led" in msg:
        client.publish("all/pico", msg)
    else:
        print("No action for message")


mqtt = MqttMicroprocessor(config_file="./mqtt_config.json")
client = mqtt.create_client(SUB_TOPIC, on_message)


print("MQTT Client Connected")

time.sleep(5)
def main():
    try:
        while True:
            # Check for new messages and handle them
            try:
                client.check_msg()
            except OSError as e:
                print("Error checking message:", e)

            time.sleep(1)
            mqtt.check_connection(client)
            

    except KeyboardInterrupt:
        pass
    finally:
        # Disconnect from the broker
        client.disconnect()


main()

    
    





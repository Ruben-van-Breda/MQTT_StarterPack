import mqtt_foudation.micropython.mqtt_microprocessor as mqtt
import time
import mqtt_foudation.micropython.examples.pico_speaker.led_device as DEVICE_LED
import mqtt_foudation.micropython.examples.pico_speaker.buzzer as DEVICE_BUZZER

# MQTT SETTINGS
SUB_TOPIC = b"all/test"

print("--------JAR Technologies------")

print("MQTT Client Created")

def on_message(topic, msg):
    print('Received message:', msg, 'on topic:', topic)
    msg = msg.decode("utf-8")

    if "led" in msg:
        DEVICE_LED.on_message(msg)
    if "buzzer" in msg:
        DEVICE_BUZZER.on_message(msg)
    else:
        print("No action for message")


client = mqtt.create_client(b"all/#", on_message)

print("MQTT Client Connected")

time.sleep(2)
def main():
    try:
        while True:
            # Check for new messages and handle them
            client.check_msg()
            time.sleep(1)
            mqtt.check_connection(client)

    except KeyboardInterrupt:
        pass
    finally:
        # Disconnect from the broker
        client.disconnect()


main()

    
    



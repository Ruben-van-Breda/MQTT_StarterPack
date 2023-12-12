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

def on_message(client, userdata, msg):
    print("\nMessage received: " + str(msg.payload.decode("utf-8")))
    print("Message topic: " + msg.topic)

def main():
    mqtt_client = MQTTStandard(config_file="mqtt_config.json", on_message=on_message)
    mqtt_client.connect()
    mqtt_client.setup_depricated()
    mqtt_client.start()

    while True:
        # sleep for 1 ms
        time.sleep(1)
        message = input("Enter message: ")
        
        if message.lower() in ["stop", "exit"]:
            break

     
        try:
            mqtt_client.publish("all/test", message, qos=1)
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    main()

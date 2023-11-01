"""
    This is a basic example using the Mqtt Library on a microprocessor running micropython.
    Created by Ruben van Breda
    Date: 1 Nov 2023
"""

from mqtt_foudation.micropython.mqtt_microprocessor import MqttMicroprocessor
import time
print("--------JAR Technologies------")


# Mqtt microprocessor settings
""" define the subtopic for your device to listen too. """
SUB_TOPIC = b"all/esp32"

# define a callback function to be called when the device receives a message
def on_message(topic, msg):
    print('Received message:', msg, 'on topic:', topic)
    msg = msg.decode("utf-8")
    # Your logic goes here...
    

""" 
Create the MQTT object:
A mqtt_config .json file can be passed in to configure the device and connect 
to the broker. If no config file is passed in, arguments can be passed in to configure.
"""
mqtt = MqttMicroprocessor(config_file="./mqtt_config.json")
# Create the client connection using the sub topic and callback function
client = mqtt.create_client(SUB_TOPIC, on_message)

time.sleep(5)

"""
    In the main loop we create a infinite loop to check for new messages and handle them
"""
def main():
    print("Mqtt Client has be created successfully")
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

if __name__ == "__main__":
    print("Starting mqtt device.")
    main()

    
    





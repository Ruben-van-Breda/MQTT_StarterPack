# Documentation

Mqtt_Foundation is a library that provides classes to communicate with a Mqtt Broker 
for a 
- web server and for your IOT devices, example:
- raspberry pico
- NodeMCU Esp32
development boards.

## Configuration
Using a configuration file, you can configure your configuration for the broker using the following  and options in a json file.
```json
{
    "CLIENT_ID": "example_id",
    "BROKER_SERVER": "broker.url",
    "BROKER_PORT": 8883,
    "BROKER_USERNAME": "username",
    "BROKER_PASSWORD": "password",
    "SUB_TOPIC": "test/",
    "PUB_TOPIC": "test/",
    "WIFI_SSID": "mywifissid",
    "WIFI_PASSWORD": "password",
}

```
#### Using the config file
Micropython
```python
mqtt = MqttMicroprocessor(config_file="./mqtt_config.json")
```
Desktop
```python
mqtt = MQTTStandard(config_file="./mqtt_config")
```

#### Using the constructor arugments
If you dont want to use the config file you can use the following

- Microprocessor
    ```python
    mqtt = MqttMicroprocessor(broker="", port=1883, client_id="esp32", username="", password="",wifi_password="", wifi_ssid="")
    ```
- Desktop
    ```python
    mqtt_client = MQTTStandard(broker_server=broker, broker_port=int(port), broker_username=username, broker_password=password,
                                        sub_topic="all/#", pub_topic="all/test" , on_message=on_message_received )
    ```
## Creating a callback function for when a message is received
```python
def on_message_received(topic, message):
    print("Hello world! I received a message")
    print("TOPIC: ", topic)
    print("MSG: ", message)
```

## Creating the client connection

```python
client = mqtt.connect(SUB_TOPIC, on_message_received)
```


## Running the client
```python
while True:
    # Check for new messages and handle them
    try:
        client.check_msg()
    except OSError as e:
        print("Error checking message:", e) 
    time.sleep(1)
    mqtt.check_connection(client)
```
import machine
from machine import Pin
import time
from time import sleep

led = Pin(15, Pin.OUT)
led.off()


def on_message(msg):
    print("DEVICE_ACTION: Recieved message:", msg)
    if "on" in msg:
        led.on()
    else:
        led.off()

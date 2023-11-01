import machine
from machine import Pin, PWM
import time
from time import sleep

buzzer = PWM(Pin(13))


# Set the frequency of the buzzer
buzzer.freq(2000)  # 2000 Hz

def beep(duration_ms):
    # Activate the buzzer
    buzzer.duty_u16(32768)  # 50% duty cycle (range is 0-65535)
    # Wait for the specified duration
    time.sleep_ms(duration_ms)
    # Deactivate the buzzer
    buzzer.duty_u16(0)


def play_note(note_frequency, note_duration):
    if note_frequency > 0:
        buzzer.freq(note_frequency)
        buzzer.duty_u16(32768)  # 50% duty cycle
    else:
        buzzer.duty_u16(0)  # 0% duty cycle for a rest
    time.sleep_ms(note_duration)
    buzzer.duty_u16(0)  # Turn off between notes


def song():
    # Define the melody (note frequency in Hz, note duration in ms)
    melody = [
        (262, 500),  # C4
        (294, 500),  # D4
        (330, 500),  # E4
        (349, 500),  # F4
        (392, 500),  # G4
        (440, 500),  # A4
        (494, 500),  # B4
        (523, 500),  # C5
        (0, 500)     # Rest
    ]
    
    for note_frequency, note_duration in melody:
        play_note(note_frequency, note_duration)

def crazy_frog():
    melody = [
        (330, 200),  # E4
        (392, 200),  # G4
        (330, 200),  # E4
        (392, 200),  # G4
        (523, 400),  # C5
        (0, 100),    # Rest
        (523, 200),  # C5
        (392, 400),  # G4
        (0, 100),    # Rest
        (392, 200),  # G4
        (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (294, 200),  # D4
        (262, 400),  # C4
    ]
    
    for note_frequency, note_duration in melody:
        play_note(note_frequency, note_duration)

def song1():
    melody = [
             (392, 200),  # G4
        (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (294, 200),  # D4
        (262, 400),  # C4
           (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (294, 200),  # D4
                     (392, 200),  # G4
        (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (294, 200),  # D4
        (262, 400),  # C4
           (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (294, 200),  # D4
    ]
    
    for note_frequency, note_duration in melody:
        play_note(note_frequency, note_duration)

def song2():
    melody = [
             (392, 200),  # G4
        (330, 400),  # E4
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (0, 100),    # Rest
        (330, 200),  # E4
        (294, 400),  # D4
        (0, 100),    # Rest
        (0, 100),    # Rest
        (294, 200),  # D4
                     (392, 200),  # G4
        (330, 400),  # E4
        (0, 100),    # Rest
      
  
        (294, 200),  # D4
    ]
    
    for note_frequency, note_duration in melody:
        play_note(note_frequency, note_duration)

def on_message(msg):
    print("Buzzer Device recieved message: ", msg)
    
    
    if "buzz" in msg:
        beep(500)
    if "crazy_frog" in msg:
        crazy_frog()
    if "song1" in msg:
        song1()
    if "song2" in msg:
        song2()
    else:
        beep(200)
    


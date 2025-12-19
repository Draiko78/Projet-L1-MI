import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Global state
_last_button_state = GPIO.LOW

def is_button_pressed():
    """Returns True if button was just pressed (edge detection)"""
    global _last_button_state
    
    current_state = GPIO.input(18)
    
    # Check for rising edge: LOW -> HIGH transition
    if current_state == GPIO.HIGH and _last_button_state == GPIO.LOW:
        _last_button_state = current_state
        return True
    
    _last_button_state = current_state
    return False

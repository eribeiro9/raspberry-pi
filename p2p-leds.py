from gpiozero import Button, LED
from TcpServerNode import Node
import time

# CONFIG
MY_LED_PIN = 17
MY_BUTTON_PIN = 19
MY_IP = 'localhost'
MY_PORT = 10000
OTHER_LED_PIN = 27
OTHER_IP = '1.2.3.4'
OTHER_PORT = 10000
SLEEP_SEC = 0.2

# VARIABLES
node = None
other_button_pressed = False

# SETUP GPIO
my_led = LED(MY_LED_PIN)
my_button = Button(MY_BUTTON_PIN)
other_led = LED(OTHER_LED_PIN)

# TODO: NETWORK CALLBACK

# SETUP P2P NETWORK

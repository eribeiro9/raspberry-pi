import RPi.GPIO as GPIO
from TcpServerNode import Node
import time

# CONFIG
LOCAL_LED_PIN = 11 #GPIO17
LOCAL_BUTTON_PIN = 35 #GPIO19
LOCAL_IP = 'localhost'
LOCAL_PORT = 10000
REMOTE_LED_PIN = 13 #GPIO27
REMOTE_IP = '192.168.1.158'
REMOTE_PORT = 10000
SLEEP_SEC = 0.2

# VARIABLES
node = None
connected_to_remote = False
remote_button_pressed = False

# SETUP GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LOCAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup([LOCAL_LED_PIN, REMOTE_LED_PIN], GPIO.OUT, initial=GPIO.LOW)

# NETWORK CALLBACK
def on_network_callback(event, node, other, data):
    global connected_to_remote
    global remote_button_pressed
    print("Event Node 1 (" + node.id + "): %s: %s" % (event, data))
    if event == "CONNECTEDWITHNODE":
        connected_to_remote = True
    elif event == "NODEINBOUNDCLOSED" or event == "NODEOUTBOUNDCLOSED":
        connected_to_remote = False
    elif event == "NODEMESSAGE":
        remote_button_pressed = data.value

# SETUP P2P NETWORK
node = Node(LOCAL_IP, LOCAL_PORT, on_network_callback)
node.start()
node.connect_with_node(REMOTE_IP, REMOTE_PORT)

def button_press(pin):
    GPIO.output(LOCAL_LED_PIN, not GPIO.input(pin))
    node.send_to_nodes({ "value": not GPIO.input(pin) })

GPIO.add_event_detect(LOCAL_BUTTON_PIN, GPIO.BOTH, callback=button_press)

# MAIN LOOP
try:
    while (1):
        time.sleep(1e6)

finally:
    GPIO.cleanup()

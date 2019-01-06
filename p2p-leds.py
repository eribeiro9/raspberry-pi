from gpiozero import Button, LED
from TcpServerNode import Node
import time

# CONFIG
LOCAL_LED_PIN = 17
LOCAL_BUTTON_PIN = 19
LOCAL_IP = 'localhost'
LOCAL_PORT = 10000
REMOTE_LED_PIN = 27
REMOTE_IP = '1.2.3.4'
REMOTE_PORT = 10000
SLEEP_SEC = 0.2

# VARIABLES
node = None
remote_button_pressed = False

# SETUP GPIO
local_led = LED(LOCAL_LED_PIN)
local_button = Button(LOCAL_BUTTON_PIN)
remote_led = LED(REMOTE_LED_PIN)

# TODO: NETWORK CALLBACK
def on_network_callback(event, node, other, data):
    print("Event Node 1 (" + node.id + "): %s: %s" % (event, data))

# SETUP P2P NETWORK
node = Node(LOCAL_IP, LOCAL_PORT, on_network_callback)
node.start()
node.connect_with_node(REMOTE_IP, REMOTE_PORT)

# MAIN LOOP
while (1):
    # HANDLE LOCAL LED
    if (local_button.is_pressed):
        local_led.on()
        node.send_to_nodes({"type": "message", "message": True})
    else:
        local_led.off()
        node.send_to_nodes({"type": "message", "message": False})
    
    # HANDLE REMOTE LED
    if (remote_button_pressed):
        remote_led.on()
    else:
        remote_led.off()
    
    time.sleep(SLEEP_SEC)
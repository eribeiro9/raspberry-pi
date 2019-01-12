import RPi.GPIO as GPIO
import socket
from threading import Thread
  
# CONFIG
LOCAL_LED_PIN = 11 #GPIO17
LOCAL_BUTTON_PIN = 35 #GPIO19
LOCAL_PORT = 10000
REMOTE_LED_PIN = 13 #GPIO27
#REMOTE_IP = '73.128.178.46'#'192.168.1.158'#'73.128.178.46'#'47.205.79.97'
REMOTE_IP = '47.205.79.97'
REMOTE_PORT = 10000

# VARIABLES
connected_to_remote = False
remote = None

# SETUP GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LOCAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup([LOCAL_LED_PIN, REMOTE_LED_PIN], GPIO.OUT, initial=GPIO.LOW)

def button_press(pin):
    global connected_to_remote, client
    GPIO.output(LOCAL_LED_PIN, not GPIO.input(pin))
    if connected_to_remote:
        client.sendall(bytes([not GPIO.input(pin)]))

GPIO.add_event_detect(LOCAL_BUTTON_PIN, GPIO.BOTH, callback=button_press)

# START TCP SERVER
def create_server():
    global remote
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', LOCAL_PORT))
    server.listen(1)
    remote, addr = server.accept()
    print('Connected', addr)
    
    while 1:
        try:
            data = remote.recv(1024)

            if not data: break
            
            value = int.from_bytes(data, byteorder='big')
            print('Client Says', value)
            
            GPIO.output(REMOTE_LED_PIN, value == 1)

        except socket.error:
            print('Error Occured.')
            break

thread = Thread(target = create_server, args = ())
thread.start()

# START CONNECTION TO REMOTE
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not connected_to_remote:
    try:
        client.connect((REMOTE_IP, REMOTE_PORT))
        connected_to_remote = True
        
    except:
        pass

# MAIN LOOP
try:
    while 1:
        sleep(10)

except KeyboardInterrupt:
    remote.close()
    GPIO.cleanup()

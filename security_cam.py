from models import ServoDriver
import socketio
import time


servo_horizontal = 0
servo_vertical = 1
driver = ServoDriver()
SERVER = 'http://192.168.0.201:5000'
connected = False


hor_pos = 90
ver_pos = 90
driver.move_to_degree(servo_vertical, ver_pos)
driver.move_to_degree(servo_horizontal, hor_pos)

sio = socketio.Client(logger = True,)

while not connected:
    try:
        sio.connect(SERVER)
    except Exception as e:
        print('error')
        print(e)
    else:
        connected = True
        print('connected')
        sio.sleep(2)
    

print(ver_pos)
@sio.on("move_camera")   ## BUG -  Limit ver_pos and hor_pos to 0 - 180
def move(data):
    global ver_pos
    global hor_pos
    if data["direction"] =="up":
        ver_pos -= 2.5
        driver.move_to_degree(servo_vertical, ver_pos)
    elif data["direction"] =="down":
        ver_pos += 2.5
        driver.move_to_degree(servo_vertical, ver_pos)
    elif data["direction"] =="left":
        hor_pos += 2.5
        driver.move_to_degree(servo_horizontal, hor_pos)
    else:
        hor_pos -= 2.5
        driver.move_to_degree(servo_horizontal, hor_pos)
    print('moving in {0} direction '.format(data['direction']))



from models import ServoDriver
import socketio


servo_horizontal = 0
servo_vertical = 1
driver = ServoDriver()
SERVER = 'http://192.168.0.201:5000'
connected = False


sio = socketio.Client()



while not connected:
    try:
        sio.connect(SERVER)
    except Exception as e:
        print('error')
        print(e)
    else:
        connected = True
        print('connected')
        sio.emit('connection_ack', {"name":"camera"})


# @sio.on('move_camera')
# def move_camera(data):
#     print(data)

    
@sio.on("move_camera")
def move(data):
    print(data)
    if data["direction"] =="up":
        driver.move_by_degree(servo_vertical, -2.5)
    elif data["direction"] =="down":
        driver.move_by_degree(servo_vertical, 2.5)
    elif data["direction"] =="left":
        driver.move_to_degree(servo_horizontal,2.5)
    else:
        driver.move_to_degree(servo_horizontal,-2.5)
    print('moving in {0} direction '.format(data['direction']))



from models import ServoMotor
import socketio


servo_horizontal = ServoMotor()
servo_vertical = ServoMotor(1)
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
        servo_vertical.move_by_degree(-2.5)
    elif data["direction"] =="down":
        servo_vertical.move_by_degree(2.5)
    elif data["direction"] =="left":
        servo_horizontal.move_by_degree(-2.5)
    else:
        servo_horizontal.move_by_degree(2.5)
    print('moving in {0} direction '.format(data['direction']))



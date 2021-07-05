# import RPi.GPIO as GPIO
import socketio
import time
import pickle
from models import Room

print(socketio.__version__)

RELAY = 11
SERVER = 'http://localhost:5000'
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(RELAY, GPIO.OUT)
# GPIO.output(RELAY, GPIO.LOW)



room = Room()
room.load()


sio = socketio.Client()
connected = False

while not connected:
    try:
        sio.connect(SERVER)
    except Exception as e:
        print('error')
        print(e)
    else:
        connected = True
        print('connected')
        sio.emit('connection_ack', room.__dict__)


@sio.on('connect')
def connection_event():
    print("connected sending ack to server")
    sio.emit('connection_ack', room.__dict__)


@sio.on('execute_request')
def execute(data):
    print(data)





room_event = 'test_room'
@sio.on(room_event)
def handle_test(data):
    print(data)



# @sio.on('water-pump-room-relay')
# def handle(data):
#     print('recd from server')
#     relay_on = relays[11]
#     if relay_on:
#         GPIO.output(RELAY, GPIO.LOW)
#         relays[11] = False
#     else:
#         GPIO.output(RELAY, GPIO.HIGH)
#         relays[11] = True

import socketio
import time
import pickle
from models import Room


RELAY = 11
SERVER = 'http://192.168.0.201:5000'



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
        print(type(room.relays[0]))
        room_dict = room
        print(type(room.relays[0]))
        room_dict.relays = [relay.__dict__ for relay in room_dict.relays]
        print(type(room.relays[0]))
        sio.emit('connection_ack', room_dict.__dict__)
        print(type(room.relays[0]))


@sio.on('connect')
def connection_event():
    print("connected sending ack to server")
    print(type(room.relays[0]))
    room_dict = room
    room_dict.relays = [relay.__dict__ for relay in room_dict.relays]
    sio.emit('connection_ack', room_dict.__dict__)


@sio.on('execute_request')
def execute(data):
    print(data)
    print(type(room.relays[0]))
    for relay in room.relays:
        if relay.pin == int(data['relay']):
            relay.toggle()





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

import socketio
import time
import pickle
from models import Room
from copy import deepcopy
import RPi.GPIO as GPIO
import asyncio
from models import TemperatureHumiditySensor


SERVER = 'http://192.168.0.201:5000'
room = Room()
temp_hum = TemperatureHumiditySensor()
room.load()
connected = False
user_toggle = False  ##True, if user viewing room on browser (flag for background tasks)


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
        room_dict = deepcopy(room)
        room_dict.relays = [relay.__dict__ for relay in room_dict.relays]
        sio.emit('connection_ack', room_dict.__dict__)


@sio.on('connect')
def connection_event():
    print("connected sending ack to server")
    room_dict = deepcopy(room)
    room_dict.relays = [relay.__dict__ for relay in room_dict.relays]
    sio.emit('connection_ack', room_dict.__dict__)


@sio.on("toggle_room_sensors")
def toggle_sensors():
    task = sio.start_background_task(sensor_data, temp_hum)
    print('starting background task')


@sio.on('execute_request')
def execute(data):
    print(data)
    for relay in room.relays:
        if relay.pin == int(data['relay']):
            relay.toggle()


def sensor_data(sensor):
    while sensor.active:
        values = sensor.get_data()
        sio.emit('process_sensor_data', values)
        sio.sleep(sensor.delay*60)



room_event = 'test_room'
@sio.on(room_event)
async def handle_test(data):
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
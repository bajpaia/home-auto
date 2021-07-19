
import socketio
import time
import json
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


def get_room():
    room_dict = deepcopy(room)
    room_dict.relays = [relay.__dict__ for relay in room_dict.relays]
    room_dict = room_dict.__dict__
    return room_dict


while not connected:
    try:
        sio.connect(SERVER)
    except Exception as e:
        print(e)
    else:
        connected = True
        print('connected')
        room_json = get_room()
        sio.emit('connection_ack', room_json)


@sio.on('connect')
def connection_event():
    print("connected sending ack to server") 
    room_json = get_room()
    sio.emit('connection_ack', room_json)

@sio.on('change_room_name')
def name_change(data):
    room.name = data["name"]
    room.save()
    room_json = get_room()
    sio.emit('connection_ack', room_json)


@sio.on("toggle_room_sensors")
def toggle_sensors():
    task = sio.start_background_task(get_sensor_data, temp_hum)


@sio.on('execute_request')
def execute(data):
    for relay in room.relays:
        if relay.pin == int(data['relay']):
            relay.toggle()
            room_json = get_room()
            sio.emit('connection_ack', room_json)
    


@sio.on('change_relay_names')
def change_name_relay(data):   
    for relay in room.relays:
        if data['relay']==relay.pin and len(data['name'])>0:
            relay.name = data['name']

    room.save()
    room_json = get_room()
    sio.emit('connection_ack', room_json)



def get_sensor_data(sensor):
    while sensor.active:
        values = sensor.get_data()
        sio.emit('process_sensor_data', values)
        sio.sleep(sensor.delay*60)





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
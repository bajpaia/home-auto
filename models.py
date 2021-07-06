import RPi.GPIO as GPIO
import Adafruit_DHT
import pickle
from threading import Thread, Event
from time import sleep

class Relay:
    def __init__(self, pin=11, name='Switch'):
        self.name = name
        self.pin = pin
        self.active = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        if self.active:
            self.active = False
            GPIO.output(self.pin, GPIO.LOW)
            print('relay {0} off'.format(self.pin))

        else:
            self.active = True
            GPIO.output(self.pin, GPIO.HIGH)
            print('relay {0} on'.format(self.pin))

    def is_active(self):
        return self.active


    def __eq__(self, other):
        assert type(other) is int, "Only integer values can be compared with relay"
        if self.pin == other:
            return True    
        return False

    def __repr__(self):
        return 'Name:{0} \n Pin:{1}'.format(self.name, self.pin)




class TemperatureHumiditySensor:
    def __init__(self, pin=4):
        self.device = Adafruit_DHT.DHT11
        self.pin = pin
        self.thread_stop_event = Event()
        self.values = {"temperature":0, "humidity":0}
    
    def get_value():
        while not self.thread_stop_event.isSet():
            values["humidity"], values["temperature"] = Adfruit_DHT.read_retry(self.device, self.pin)
            time.sleep(60)


    def __eq__(self, other):
        assert type(other) is int, "Only integer values can be compared with sensor"
        if self.pin == other:
            return True    
        return False

    



class Room:
    def __init__(self, name="Room"):
        self.name = name
        self.code = name.lower().replace(' ', '-')
        self.relays = list()
        self.sensors = list()

        

    def add_relays(self, relays):
        if type(relays) == type(Relay()):
            self.relays.append(relays)
        elif type(relays) == list:
            self.relays += [relay for relay in relays]


    def __repr__(self):
        return 'Room: {0}'.format(self.name)


    def __eq__(self, other):
        assert type(other) is str, "Only String values can be compared with Room"
        if self.code == other:
            return True    
        return False

    
    def load(self):
        f = open('room_config.pickle', 'rb')
        tmp_dict = pickle.load(f)
        f.close()          
        self.__dict__.clear()
        self.__dict__.update(tmp_dict) 


    def save(self):
        f = open('room_config.pickle', 'wb')
        pickle.dump(self.__dict__, f)
        f.close()




class PiClient:
    def __init__(self, server_address, room):
        self.connected = False
        self.server_address = server_address
        self.sio = socketio.Client()
        self.room = room
        while not self.connected:
            try:
                self.sio.connect(self.server_address)
            except Exception as e:
                print(e)
            else:
                self.connected = True
                print('connected')
                self.sio.emit('connection_ack', self.room.__dict__)

            
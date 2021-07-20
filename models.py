import RPi.GPIO as GPIO
import Adafruit_DHT
import pickle
from threading import Thread, Event
from time import sleep
from copy import deepcopy
from PCA9685 import PCA9685



class Relay:
    

    def __init__(self, pin=11, name='Switch'):
        self.name = name
        self.pin = pin
        self.active = True


    def toggle(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
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
        if len(self.relays)>0:
            for relay in self.relays:
                relay.toggle()


    def save(self):
        f = open('room_config.pickle', 'wb')
        pickle.dump(self.__dict__, f)
        f.close()


class TemperatureHumiditySensor:
    
    def __init__(self, pin=4, delay_mins = 1):
        self.device = Adafruit_DHT.DHT11
        self.pin = pin
        self.delay = delay_mins
        self.active = True
        self.values = {"temperature":0, "humidity":0}


    def get_data(self):
        self.values["humidity"], self.values["temperature"] = Adafruit_DHT.read_retry(self.device, self.pin)
        self.values["humidity"], self.values["temperature"] = str(self.values["humidity"])+ '%', str(self.values["temperature"]) +'℃'
        return self.values


    def toggle(self):
        if self.active:
            self.active = False
        else:
            self.active = True 


    def __eq__(self, other):
        assert type(other) is int, "Only integer values can be compared with sensor"
        if self.pin == other:
            return True    
        return False



class ServoDriver:

    def __init__(self, channel=0, init_pulse=1500):
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)
    

    def degree_to_pulse(self, degrees):
        return degrees*11.11

    
    def move_by_degree(self, channel,degrees):
        pulse = self.degree_to_pulse(degrees)
        self.move_by_pulse(channel, pulse)
            

    def move_by_pulse(self, channel,pulse):
        self.pwm.setServoPulse(channel, pulse)
        sleep(0.01)
        print("Pulse: {0}".format(pulse))



    def move_to_degree(self, channel,degree):
        pulse = self.degree_to_pulse(degree)+500
        self.move_by_pulse(channel, pulse)
        


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


# class SecurityCamera:

#     def __init__(self):

            
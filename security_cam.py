from PCA9685 import PCA9685
import time

def move_Servo(channel, pulse):
    pwm.setServoPulse(channel,pulse) 
    time.sleep(0.05)  



pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)



class ServoMotor:

    def __init__(self, channel=0, init_pulse=1500):
        self.pwm = PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)
        self.channel = channel
        self.position = init_pulse
    

    def degree_to_pulse(self, degrees):
        return degree*11.11

    
    def move_servo(self, pulse):
        self.pwm.setServoPulse(self.channel, pulse)
        self.position += pulse
        time.sleep(0.1)


if __name__ == '__main__':
    servo1 = ServoMotor()
    servo2 = ServoMotor(1)

    for i in range(500, 2580, 11):

        servo1.move_servo(i)
        time.sleep(1)
        servo2.move_servo(i)
    servo1.move_servo(1500)
    tim.sleep(1)
    servo2.move_servo(1500)      


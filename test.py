from models import ServoMotor


servo_horizontal = ServoMotor()
servo_vertical = ServoMotor(1)

if __name__ == '__main__':
    

    for i in range(500, 2580, 11):
        servo1.move_servo(i)
        servo2.move_servo(i)
    servo1.move_servo(1500)
    time.sleep(0.01)
    servo2.move_servo(1500)      

from models import ServoMotor


servo_horizontal = ServoMotor()
servo_vertical = ServoMotor(1)

if __name__ == '__main__':
    

    for i in range(500, 2580, 11):
        servo_horizontal.move_by_pulse(i)
        servo_vertical.move_by_pulse(i)
    servo_horizontal.move_by_pulse(1500)
    time.sleep(0.01)
    servo_vertical.move_by_pulse(1500)      

from models import ServoMotor
import time

servo_horizontal = ServoMotor(init_pulse = 1500)
servo_vertical = ServoMotor(1, 1500)

if __name__ == '__main__':
    

    # for i in range(500, 2580, 11):
    #     servo_horizontal.move_by_pulse(i)
    #     servo_vertical.move_by_pulse(i)
    # servo_horizontal.move_by_pulse(1500)
    # time.sleep(0.01)
    # servo_vertical.move_by_pulse(1500)    

    for i in range(0, 180, 2):
        servo_horizontal.move_to_degree(i)
        servo_vertical.move_to_degree(i)
    servo_horizontal.move_to_degree(90)
    time.sleep(0.01)
    servo_vertical.move_to_degree(90)     

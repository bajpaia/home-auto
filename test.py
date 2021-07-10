from models import ServoDriver
import time

driver = ServoDriver()
servo_horizontal = 0
servo_vertical = 1

if __name__ == '__main__':
    # for i in range(500, 2580, 11):
    #     driver.move_by_pulse(servo_horizontal,i)
    #     driver.move_by_pulse(servo_vertical,i)

    # driver.move_by_pulse(servo_horizontal, 1500)
    # time.sleep(0.20)
    # driver.move_by_pulse(servo_vertical, 1500)    

    for i in range(0, 180, 2):
        driver.move_to_degree(servo_horizontal,i)
        driver.move_to_degree(servo_vertical, i)
    driver.move_to_degree(servo_horizontal,90)
    driver.move_to_degree(servo_vertical, 90)    

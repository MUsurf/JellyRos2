#!/usr/bin/env python3

'''
ROS
---

node:
----
        - motor_commander

Publishes:
---------
        - motor_command

Subscribes:
----------

'''


# BEGIN IMPORT
# import time
import numpy
import rospy
from std_msgs.msg import Int32MultiArray
# END IMPORT


'''
Goals:

Be able to run
destroy the typing abilities of my enemies
Push something
Spin up and spin down slowly

Fib sequence
'''

# num_motors = 8

# array_of_array = [
#     [20 for _ in range(num_motors)],
#     [30 for _ in range(num_motors)],
#     [40 for _ in range(num_motors)],
#     [50 for _ in range(num_motors)],
#     [40 for _ in range(num_motors)],
#     [30 for _ in range(num_motors)],
#     [20 for _ in range(num_motors)],
#     [10 for _ in range(num_motors)],
# ]

#GLOBALS
##get commander
pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
rospy.init_node('motor_commander', anonymous=True)
rate = rospy.Rate(.1) # 10hz
##motors numpy array
motors = numpy.array([0 for _ in range(8)])

def jelly_spin(motors: list,direction: str,scaler: int) -> list:
    if direction == 'right':
        pass
    elif direction == 'left':
        scaler *= -1
    else:
        print('unknown direction:',direction)
        return motors
    motors[4] = 1
    motors[7] = 1
    motors[5] = -1
    motors[6] = -1
    motors *= scaler
    return motors

def jelly_stop() -> list:
    for i in range(4):
        motors[i+4] = 0
    return motors
        
def jelly_go(motors: list,direction: str,scaler: int) -> list:
    if direction == 'forward':
        axis = 'y'
    elif direction == 'back':
        axis = 'y'
        scaler *= -1
    elif direction == 'right':
        axis = 'x'
    elif direction == 'left':
        axis = 'x'
        scaler *= -1
    else:
        print('unknown direction:',direction)
        return motors
    if axis == 'y':
        motors[4] = 1
        motors[5] = 1
        motors[6] = -1
        motors[7] = -1
    else:
        motors[4] = 1
        motors[6] = 1
        motors[5] = -1
        motors[7] = -1
    motors *= scaler
    return motors

def motor_driver(motors: list):
    rate.sleep(4)
    while not rospy.is_shutdown():
        pub.publish(data=jelly_spin(motors,'right', 50))
        rate.sleep(5)
        pub.publish(data=jelly_stop())
        pub.publish(data=jelly_go(motors,'forward', 25))
        rate.sleep(3)
        pub.publish(data=jelly_stop())
        rate.sleep(1)

motor_driver(motors)
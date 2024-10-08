#!/usr/bin/env python3

'''
ROS
---

node:
----
        - motor_driver

Publishes:
---------
        - motor_command

Subscribes:
----------

'''



# BEGIN IMPORT
import time
import rospy
from std_msgs.msg import Int32MultiArray
# END IMPORT

'''"

Goals:

Be able to run
Push something
Spin up and spin down slowly

Fib seq
'''

num_motors = 8
''' 
array_of_array = [
    [20 for _ in range(num_motors)],
    [30 for _ in range(num_motors)],
    [40 for _ in range(num_motors)],
    [50 for _ in range(num_motors)],
    [40 for _ in range(num_motors)],
    [30 for _ in range(num_motors)],
    [20 for _ in range(num_motors)],
    [10 for _ in range(num_motors)]
]
'''
def motor_driver():

    index = 0

    # pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
    # rospy.init_node('motor_driver', anonymous=True)
    # rate = rospy.Rate(.1) # 10hz
#  not rospy.is_shutdown
    while True:
        # print(array_of_array[index])

        # pub.publish(data=array_of_array[index])

        index = (index + 1) % 8 # iterates 1 through 8


        # rate.sleep()
        time.sleep(1)
# motors = [5, 6, 7, 8]
motors = [20 for _ in range (8)]


pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
rospy.init_node('motor_commander', anonymous=True)
rate = rospy.Rate(.1) # 10hz



def jelly_spin(string, seconds, scaler):
    if (string == "right"):
        scaler *= -1
    elif (string == "left"):
        pass
    else:
        return        
    motors[4] = scaler * -1
    motors[7] = scaler * -1
    motors[5] = scaler * 1
    motors[6] = scaler * 1
    for i in range(4):
        motors[i+4] = 0
    print (motors)

def jelly_go(string, scaler, seconds):
    if (string == "forwards"): 
        scaler *= -1
    else:
         pass
    motors[4] = scaler * -1
    motors[7] = scaler * -1
    motors[5] = scaler * 1
    motors[6] = scaler * 1
    time.sleep(seconds)

def motor_driver(motors: list):
    while not rospy.is_shutdown():
        pub.publish(data=jelly_spin(motors,'right',50))
        rate.sleep(5)
        pub.publish(data=jelly_go(motors, 'forwards', 50))
        rate.sleep(5)



jelly_go("forwards", 5, 1)
print(motors)
motor_driver()
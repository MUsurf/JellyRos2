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

def motor_driver():

    index = 0

    pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
    rospy.init_node('motor_driver', anonymous=True)
    rate = rospy.Rate(.1) # 10hz
#  not rospy.is_shutdown
    while True:
        # print(array_of_array[index])

        # pub.publish(data=array_of_array[index])

        index = (index + 1) % 8 # iterates 1 through 8

        # rate.sleep()
        time.sleep(1)

def motor_driver(motors: list):
    while not rospy.is_shutdown():
        pub.publish(data=jelly_turn('right', 20, 3))
        rate.sleep(5)
        pub.publish(data=jelly_go('forwards', 10, 3))
        rate.sleep(5)

motor_driver()

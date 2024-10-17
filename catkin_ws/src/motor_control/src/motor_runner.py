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


"""

! This is just a test driver function not used in comp

"""


# BEGIN IMPORT
import time
import rospy
from std_msgs.msg import Int32MultiArray
# END IMPORT

from typing import List

num_motors = 8

'''
high: List[int] = [20 for i in range(num_motors)]
low: List[int] = [30 for i in range(num_motors)]
list_thing = high
'''

motor_powers = [0 for i in range(num_motors)]

hl_counter = 0

def commander():
    global hl_counter
    pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
    rospy.init_node('motor_commander', anonymous=True)
    rate = rospy.Rate(.4) # 40hz



        # hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(list_thing)
        pub.publish(data=list_thing)

        rate.sleep()

        pub.publish(data=motor_powers)
        print('x')

        rate.sleep()


motors = [0 for _ in range (8)]

def jelly_turn(direction: str, speed: float, seconds: float):
    if (direction == "right"):
        speed *= -1
    elif (direction != "left"):
        print("invalid turn direction, try 'right' or 'left'")
        return

    motors[4] = speed * -1
    motors[7] = speed * -1
    motors[5] = speed * 1
    motors[6] = speed * 1

    print (motors)
    time.sleep(seconds)
    #stopping the turn
    for i in range(4):
        motors[i+4] = 0
    print(motors)
    # example: jelly_turn("left", 20, 3)

def jelly_go(direction: str, speed: float, seconds: float):
    if (direction == "forwards"): 
        speed *= -1
    motors[4] = speed * -1
    motors[7] = speed * -1
    motors[5] = speed * 1
    motors[6] = speed * 1
    print(motors)
    time.sleep(seconds)

    for i in range(4):
        motors[i+4] = 0
    print(motors)


# pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
# rospy.init_node('motor_commander', anonymous=True)
# rate = rospy.Rate(.1) # 10hz


# user_direction = input("State the Direction(forwards or backwords):  ")
# user_speed = int(input("state the speed(0-80):"))
# user_seconds = int(input("State the duration of motor usage(int in seconds):"))

# jelly_go(user_direction, user_speed, user_seconds)

# user_direction = input("State which direction you would like to turn(right or left):  ")
# user_speed = int(input("state the speed(0-80):"))
# user_seconds = int(input("State the duration of motor usage(int in seconds):"))

# jelly_turn(user_direction, user_speed, user_seconds)



if __name__ == '__main__':
    try:
        commander()
    except rospy.ROSInterruptException:
        pass
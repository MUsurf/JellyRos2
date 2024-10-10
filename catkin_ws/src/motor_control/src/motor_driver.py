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
# motors = [5, 6, 7, 8]
motors = [0 for _ in range (8)]


# pub = rospy.Publisher('motor_command', Int32MultiArray, queue_size=10)
# rospy.init_node('motor_commander', anonymous=True)
# rate = rospy.Rate(.1) # 10hz



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


def motor_driver(motors: list):
    while not rospy.is_shutdown():
        pub.publish(data=jelly_turn('right', 20, 3))
        rate.sleep(5)
        pub.publish(data=jelly_go('forwards', 10, 3))
        rate.sleep(5)


# user_direction = input("State the Direction(forwards or backwords):  ")
# user_speed = int(input("state the speed(0-80):"))
# user_seconds = int(input("State the duration of motor usage(int in seconds):"))

# jelly_go(user_direction, user_speed, user_seconds)

# user_direction = input("State which direction you would like to turn(right or left):  ")
# user_speed = int(input("state the speed(0-80):"))
# user_seconds = int(input("State the duration of motor usage(int in seconds):"))

# jelly_turn(user_direction, user_speed, user_seconds)

motor_driver()

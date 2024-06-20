#!/usr/bin/env python3

# BEGIN IMPORT
import busio
import time
import rospy
from typing import List
from board import SCL, SDA
import adafruit_pca9685 as PCA9685
# END IMPORT


# BEGIN SETUP
i2c = busio.I2C(SCL, SDA)
pca = PCA9685.PCA9685(i2c, address=0x28)
pca.frequency = 280  # Hz
# END SETUP

# Rospy nodes
rospy.init_node("motor_listener")
rate = rospy.Rate(100)


# BEGIN STD_MSGS
from std_msgs.msg import Int32MultiArray
# from std_msgs.msg import Bool
# END STD_MSGS


class MotorCommand():
    def __init__(self, local_channels: List[int], num_motors: int, step_size=5, minor_time=.1) -> None:
        # info Number of motors being managed
        self.motorNum: int = num_motors

        # info list can only contain -1, 0, 1
        self.motor_direction: List[int] = [1 for _ in range(num_motors)]

        # info How much to move the motors at each minor step
        self.step_size: int = step_size

        # info Set how much time to wait on arming
        self.minor_step: float = minor_time

        # info Needed to save pin states to let outside program manage interupts when driving motors
        # info As this lets us step between power levels using duty cycle 0-100
        self.pinStates: List[int] = [0 for _ in range(num_motors)]

        # info This creates an array of channels to change
        # info This is done so number of motors can be changed on the fly
        self.motors: List[PCA9685.PWMChannel] = [
            pca.channels[channel] for channel in local_channels]

    def __microSec_to_duty(self, microSec: int) -> int:
        """Convert Microsecond pulses to duty cycle

        Convert Microsecond length pulses that have been aligned with the operating requirments of the interface to duty cycle of the current PWM frequency

        Parameters
        ----------
            microSec : int
                Must be int from 0-100 'microSec'

        Returns
        -------
            int
                int from 65536-0
        """

        samp_time: float = (1/pca.frequency) * 1000 * \
            1000  # Convert to Micro Sec
        duty_cycle = int((65536 * microSec)/(samp_time))
        return duty_cycle

    def set_motor_speed(self, motor_idex: int, speed: int) -> None:
        '''Set the speed of a single motor'''

        pwm_value: int = self.__microSec_to_duty(1000 + (speed * 10))
        self.motors[motor_idex].duty_cycle = pwm_value

    def pinStep(self, targets: List[int]) -> None:
        """Move pin towards target supplied

        Generates intermediate values and then steps pin from current state toward target.

        Parameters
        ----------
            targets : List[int]
                list of targets for motors (order matters).

        Notes
        -----
            Should be used with an outside function to handle interupts
        """

        directions: List[int] = self.__targetDistance(targets)
        for index in range(len(directions)):
            if (directions[index] == 0):
                continue
            self.pinStates[index] += directions[index] * self.step_size
            print(self.pinStates[index])
        # ? Sets every pin even if it is already opperating at that speed
        # ? Don't think this is an area that needs to be improved but is an easy target
        self.__set_motors(self.pinStates)

    def __targetDistance(self, targets: List[int]) -> List[int]:
        """Figures out wich direction to step pins

        Notes
        -----
            This is a rough way to do this and can be reworked

        """
        directions: List[int] = []
        for i in range(len(targets)):
            value: int = (targets[i] - self.pinStates[i])
            if (value == 0):
                directions.append(0)
            elif (value > 0):
                directions.append(1)
            elif (value < 0):
                directions.append(-1)
            else:
                raise ValueError
        return (directions)

    def __set_motors(self, speeds: List[int]) -> None:
        """Sets pins to values given by speed position"""

        for index in range(self.motorNum):
            self.set_motor_speed(index, speeds[index])

    # ~ This is a ros function that has not been proven to work
    def callback(self, message_rec):
        """Function to subscribe to driver with ros"""

        print("Data received is: " + str(message_rec.data))
        for index in range(len(message_rec)):
            x = self.__microSec_to_duty(
                message_rec[index])

            self.motors[index].duty_cycle = x
            print(f"type of var callback {type(x)}")


class MotorInterface():
    """Handles direct control of motors
    
        Should be given an array of ints 
    """

    def __init__(self, channels: List[int], numMotors: int, offset: int, max_val: int, minor_time: float, step_size: int, steps_used=10) -> None:
        # info Number of motors
        self.numMotors: int = numMotors
        # info This is the amount of time between steps
        self.minor_time: float = minor_time
        # info This is how to set the min value
        self.offset: int = offset
        # info This is needed as this interface will take percent and scale to output used
        self.max_val: int = max_val
        # info max steps to go from one extreme to the other
        self.max_steps_needed: int = int(self.max_val / step_size)
        # info This is the amount of steps used assuming motors don't need to reach value
        self.steps_used: int = steps_used
        # info This is the instance of motorcommand that will be used
        self.motor_commander = MotorCommand(
            channels, self.numMotors, step_size, self.minor_time)

    def arm_seq(self) -> None:
        """Current method of arming all motors may change with calibration

        Notes
        -----
            Pin target values are hardcoded they should not need to be changed often.
        """

        target_speeds: List[List[int]] = [
            [0 for _ in range(self.numMotors)],
            [20 for _ in range(self.numMotors)],
            [30 for _ in range(self.numMotors)],
            [10 for _ in range(self.numMotors)]
        ]

        for targets in target_speeds:
            for _ in range(self.max_steps_needed):
                self.motor_commander.pinStep(targets)
                time.sleep(self.minor_time)

    def clo_seq(self) -> None:
        """Cleans up motors and is responsible for bringing them all back to zero"""

        num_runs: int = self.max_steps_needed + 1
        targets: List[int] = [0 for _ in range(self.numMotors)]
        for _ in range(num_runs):
            self.motor_commander.pinStep(targets)
            time.sleep(self.minor_time)

    def __percent_to_duty(self, percent: int) -> int:
        range: int = abs(self.max_val - self.offset)
        duty: int = int(((percent / 100) * range) + self.offset)
        return duty

    def calling_function(self, directions) -> None:
        """Used to step motors to each target given"""

        duty_directions: List[int] = self.direction_to_motor(directions)
        for _ in range(self.steps_used):
            self.motor_commander.pinStep(duty_directions)
            time.sleep(self.minor_time)

    def direction_to_motor(self, directions) -> List[int]:
        """This function will have some of the direction to motor commands

        Notes
        -----
            This function is not implemented yet and only contains the translation from percent drive of commands to duty cycle
        """

        drive_in_duty: list[int] = []
        for p_direction in directions:
            drive_in_duty.append(self.__percent_to_duty(p_direction))
        return (drive_in_duty)
    

    def callback(self, message_rec):
        """Function to subscribe to driver with ros"""

        print("Data received is: " + str(message_rec.data))
        self.calling_function(message_rec.data)
        # for index in range(len(message_rec)):
        #     x = self.__microSec_to_duty(
        #         message_rec[index])

        #     self.motors[index].duty_cycle = x
        #     print(f"type of var callback {type(x)}")


# Motor init codes
try:
    # Set up for 8 motors should be typical set up
    # Next thing to do is mock the motors
    local_channels: List[int] = [x for x in range(8)]
    num_motors: int = len(local_channels)
    motor_caller = MotorInterface(local_channels, num_motors, 0, 100, .1, 5)

    # high: List[int] = [20 for i in range(num_motors)]
    # low: List[int] = [30 for i in range(num_motors)]

    print("arming")
    motor_caller.arm_seq()
    print("done arming")
    while not rospy.is_shutdown():
        rospy.Subscriber("motor_command", Int32MultiArray, motor_caller.callback)
        # rospy.Subscriber("volt_low", Bool, loop.cut_motors)
        rospy.spin()
    motor_caller.clo_seq()

except KeyboardInterrupt:
    motor_caller.clo_seq()

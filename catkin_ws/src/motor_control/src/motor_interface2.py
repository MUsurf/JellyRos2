# Begin typing imports
from typing import List
from motor_commander2 import MotorCommand
import time
# End typing imports

class motor_interface():
    """Handles direct control of motors"""
    
    def __init__(self):
        #info Channel for each of 8 motors
        self.channels = [0,1,2,3,4,5,6,7]
        #info Make the motor commander
        self.motor_commander = MotorCommand(self.channels)
        
    def set_motor_powers(self, x : float, y : float, z : float, roll : float, pitch : float, yaw : float):
        """Sets the motor powers. Uses get_powers to convert to PWM percentages."""
        powers = self.get_powers(x,y,z,roll,pitch,yaw)
        self.motor_commander.set_motor_pwm(powers)
        
    def set_motor_powers_individual(self, powers : list) -> bool:
        """Sets the individual duty cycles rather than using x,y,z,roll,pitch,yaw. Returns whether the powers were set."""
        if(len(powers) == self.motor_commander.num_motors):
            self.motor_commander.goal_power = powers
            return True
        return False
            
        
    def arm_seq(self):
        """Runs the motors through a ramping sequence before turning them off."""
        arm_powers = [
            [10 for _ in range(self.motor_commander.num_motors)], 
            [20 for _ in range(self.motor_commander.num_motors)]
        ]
        arm_time = 1 # seconds
        
        for arm_power in arm_powers:
            self.set_motor_powers_individual(arm_power)
            time.sleep(arm_time)
        
        self.set_motor_powers_individual([0 for _ in range(self.motor_commander.num_motors)])
        
    def horzitonal_power(self, x : float, y : float, yaw : float) -> list:
        """Function to convert inputs for desired x, y, yaw into powers for motors 1, 2, 3, 4
            Motors 1, 2, 3, 4 (CCW starting from top right motors as seen from above)"""
        powers = [
            x - y + yaw,
            x + y - yaw,
            x - y - yaw,
            x + y + yaw
        ]
        
        return powers
    
    def vertical_power(self, roll: float, pitch: float, z: float) -> list:
        """Function to convert inputs for desired roll, pitch, z into powers for motors 5 6 7 8"""
        
        #list is read [top right, top left, bottom left, bottom right]
        powers = [
            z + roll + pitch,
            z - roll + pitch,
            z - roll - pitch,
            z + roll - pitch
        ]

        return powers
    
    def get_powers(self, x : float, y : float, yaw : float, roll: float, pitch: float, z: float) -> list:
        """Converts the 6 inputs into 8 motor powers."""
        
        powers = self.vert_power(roll, pitch, z) + self.horz_power(x, y, yaw)
        
        for i in range(len(powers)):
            if (powers[i] > 100):
                for j in range(len(powers)):
                    powers[j] / powers[i]
            
        # Sum powers into single list
        for i in range(len(powers)):
            if (powers[i] > 0):
                powers[i] = self.power_scale(powers[i]) # Negative power output is less than positive; compensate by lowering pos.
        
        return powers
    
    def get_positive_thrust(self, pow : float) -> float:
        pow = 1500 + 400 * pow # Scale to the function's 1500-1900 range
        return -0.00000002 * (pow ** 3) + 0.0001217197 * (pow ** 2) - 0.2259899999 * (pow) + 132.4283468435
    
    def get_negative_thrust(self, pow : float) -> float:
        pow = 1500 - 400 * abs(pow)
        return -0.0000000231 * (pow ** 3) + 0.0000751388 * (pow ** 2) - 0.0665160408 * (pow) + 8.8768852253
    
    def get_positive_pow(self, thrust : float) -> float:
        #Someone go do the math for the inverse pls :)
        return 0
    
    def get_negative_pow(self, thrust : float) -> float:
        #Someone go do the math for the inverse pls :)
        return 0
    
    def power_scale(self, pow : float) -> float:
        if(pow > 0):
            thrust = self.get_negative_thrust(pow)
            return self.get_positive_pow(thrust)
        else:
            thrust = self.get_positive_thrust(pow)
            return self.get_negative_pow(thrust)
    
    

# Begin typing imports
from typing import List
# End typing imports

# Begin imports
import busio
from board import SCL, SDA
import adafruit_pca9685 as PCA9685
# End imports

# BEGIN SETUP
i2c = busio.I2C(SCL, SDA)

#pca = PCA9685.PCA9685(i2c, address=0x40)
#pca.frequency = 280  # Hz
# END SETUP

class MotorCommand():
    def __init__(self,
        local_channels : List[int]) -> None:
        """Put documentation here"""
        
        #PCA definition
        self.pca = PCA9685.PCA9685(i2c, address=0x40) #0x40 is the I2C address of the PCA
        self.pca.frequency = 280 # Hz
        
        self.num_motors = len(local_channels)
        
        self.motor_duty_cycles = [0 for i in range(self.num_motors)]
        
        self.motors: List[PCA9685.PWMChannel] = [
            self.pca.channels[channel] for channel in local_channels]
        
    def axis_to_mp(self, #Name this better :(
        x : float,
        y : float,
        z : float,
        roll: float,
        pitch: float,
        yaw : float):
        """Put documentation here"""
        
        #The first 4 motor powers scaled -100 to 100
        h_powers = self.horizontal_power(x, y, yaw)
        
        #The second 4 motor powers scaled -100 to 100
        v_powers = self.vertical_power(z, roll, pitch)
        
        #Combine both groups of motors
        self.motor_duty_cycles = h_powers + v_powers
        
        #Sets motor powers
        self.set_motor_powers(self.motor_duty_cycles)
                    
    def set_motor_powers(self, powers : list = None):
        """Put documentation here"""
        
        #Sets the duty cycles to the last recorded duty cycle if nothing is provided
        #Prob not necessary but what do I know
        if(powers == None):
            powers = self.motor_duty_cycles
        
        for i in range(self.num_motors):
            """
            65535 is the 16 bit max.
            The duty cycle ranges from 0-65535 as 0-100
            NOTE: This no work right now as negative numbers are not accounted for.
            Eventaully, 0 will be -100 and 65535 will be 100
            """
            self.motors[i].duty_cycle = int(65535 * abs(powers[i]) / 100) 
        
    def horizontal_power(self, #NAME THIS BETTER :(
        x : float,
        y : float,
        yaw : float):
        """Put documentation here"""

        powers = [0,0,0,0]
        
        #Code here
        
        return powers
    
    def vertical_power(self, #NAME THIS BETTER :(
        z : float,
        roll : float,
        pitch : float):
        """Put documentation here"""

        powers = [0,0,0,0]
        
        #Code here
        
        return powers
    
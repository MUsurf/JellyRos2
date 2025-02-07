
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
        
    def horizontal_powers(self, #NAME THIS BETTER :(
        x : float,
        y : float,
        yaw : float):
        """Put documentation here"""

        powers = [x,x,x,x]
        #Code here
        
        powers[0] += -y+yaw
        powers[1] += y-yaw
        powers[2] += -y-yaw
        powers[3] += y+yaw

        max = 0
        
        for i in powers:
            if (abs(powers[i])>max):
                max = abs(powers[i])

        if(max>100):
            for j in powers:
                powers[j] = (powers[j]/max) * 100
       

        
        return powers
    
    def veritcal_power(self, 
        z : float,
        roll : float,
        pitch : float):
        """Put documentation here"""

        #like reading, 5, 6, 7, 8 (aka 5 is top left and 8 is bottom right)
        powers = [0,0,0,0]
        
        powers = [z, z, z, z]

        #counterclockwise is positive
       
        powers[0] -= roll
        powers[1] += roll
        powers[2] -= roll
        powers[3] += roll

        powers[0] += pitch
        powers[1] += pitch
        powers[2] -= pitch
        powers[3] -= pitch

        #increases negative powers by 25% before averaging
        for i in powers:
            if i < 0:
                i *= 1.25
        
        maxPower = powers[0]
        for i in range(len(powers)-1):
            if abs(powers[i]) > maxPower:
                maxPower = abs(powers[i])
        
        if maxPower > 100:
            for i in powers:
                powers[i] = (powers[i]/maxPower)*100

        #Code here
        
        return powers
    
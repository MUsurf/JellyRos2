
# Begin typing imports
from typing import List
# End typing imports

# Begin imports
import busio
from board import SCL, SDA
import adafruit_pca9685 as PCA9685
from threading import Thread
import time
# End imports

# BEGIN SETUP
i2c = busio.I2C(SCL, SDA)

#pca = PCA9685.PCA9685(i2c, address=0x40)
#pca.frequency = 280  # Hz
# END SETUP

class MotorCommand():
    """Put class documentation here"""
    def __init__(self,
        local_channels : List[int]) -> None:
        """Put documentation here"""
        
        #PCA definition
        self.pca = PCA9685.PCA9685(i2c, address=0x40) #0x40 is the I2C address of the PCA
        self.pca.frequency = 280 # Hz
        
        self.num_motors = len(local_channels)
        
        self.current_power = [0 for i in range(8)]
        self.goal_power = [0 for i in range(8)]
        self.step_value = 1
        self.motor_duty_cycles = [0 for i in range(self.num_motors)]
        
        self.motors: List[PCA9685.PWMChannel] = [
            self.pca.channels[channel] for channel in local_channels]
        
        self.motor_flag : bool = True
        self.motor_update_frequency = 50
        self.motor_thread : Thread = Thread(self.motor_loop)
        self.motor_thread.start()
    
    def set_motor_pwm(self, powers : list):
        
        #this is how duty cycle is set: self.motors[motor_idex].duty_cycle = pwm_value
        #pwm_value is a 16 bit int (0 is -100, max is 100)
        
        
        
    def power_stepping(self):
        pass
    
    def motor_loop(self):
        while True:
            start_time = time.time()
            if(self.motor_flag):
                self.power_stepping()
                self.set_motor_pwm(self.current_power)
            if(time.time() - start_time < 1 / self.motor_update_frequency):
                time.sleep(1 / self.motor_update_frequency - (time.time() - start_time))
        
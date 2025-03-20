
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
    """Put class documentation here
    """
    def __init__(self,
        local_channels : List[int],
        pca_address : int = 0x40) -> None:
        """_summary_

        _extended_summary_

        Parameters
        ----------
        local_channels : List[int]
            List of channels to be using from i2c splitter (?)
        pca_address : int
            Address of the pca (?)
        """
        
        #PCA definition
        self.pca = PCA9685.PCA9685(i2c, address=pca_address) #0x40 is the I2C address of the PCA
        self.pca.frequency = 280 # Hz
        
        # info Number of motors being managed
        self.num_motors = len(local_channels)
        
        # info Current power of motors
        self.current_power = [0 for i in range(8)]
        # info Desired power of motors
        self.goal_power = [0 for i in range(8)]
        # info Step value to alter power by
        self.step_value = 1
        
        self.motors: List[PCA9685.PWMChannel] = [
            self.pca.channels[channel] for channel in local_channels]
        
        self.motor_flag : bool = True
        self.motor_update_frequency = 50 # hz
        self.motor_thread : Thread = Thread(self.motor_loop)
        
        #Should it be started here?
        self.motor_thread.start()
    
    def set_motor_pwm(self, powers : list):
        """Set the PWM signal for the motors. inputs are from -100 to 100, which are basically percentages of the total
        This converts the input to a format the motor actaally wants.
        """
        #0 (-100) to 65535 (100)
        # #pwm_value is a 16 bit int (0 is -100, max is 100)
        
        for i in range(len(powers)):
            duty_cycle = ((self.current_power[i] + 100) / 200.0) * 65535
            self.motors[i].duty_cycle = duty_cycle
        
    def power_stepping(self):
        """Ensures a motor's power increases in steps instead of trying to blast full power."""
        for i in range(len(self.current_power)):
            distance = self.goal_power[i] - self.current_power[i]
            if not distance == 0:
                if(abs(distance) <= self.step_value):
                    self.current_power[i] = self.goal_power[i]
                else:
                    self.current_power[i] += (distance / abs(distance)) * self.step_value
    
    def motor_loop(self):
        """Refreshes the motor's PWM signal at a set frequency. Constantly."""
        while True:
            start_time = time.time()
            if(self.motor_flag):
                try:
                    self.power_stepping()
                    self.set_motor_pwm(self.current_power)
                except:
                    # Not really sure how this should be handled. Exceptions wouldn't really propagate up.
                    # Maybe set @self.motor_flag to false? Although that doesn't really help
                    # Definitely want a way for it to be reported. Shouldn't kill the thread though
                    pass
            if(time.time() - start_time < 1 / self.motor_update_frequency):
                time.sleep(1 / self.motor_update_frequency - (time.time() - start_time))
        
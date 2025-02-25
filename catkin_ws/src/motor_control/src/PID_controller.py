import time

class PIDController:
    def __init__(self, kP : float, kI : float, kD : float):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.last_time = None
        self.error_accum = 0
        self.last_error = None
        
    def __init__(self,
                 setpointX : float, measurementX : float,
                 setpointY : float, measurementY : float,
                 setpointZ : float, measurementZ : float,
                 setpointRoll : float, measurementRoll : float,
                 setpointPitch : float, measurementPitch : float,
                 setpointYaw : float, measurementYaw : float,
                 X_power : float = None, Y_power : float = None, Z_power : float = None,
                 Roll_power : float = None, Pitch_power : float = None, Yaw_power : float = None
                ):
        print("ur mom")
        
        
    def calculate(self, setpoint : float, measurement : float):
        #This probably works
        output : float = 0.0 #power
        error = setpoint - measurement
        
        if (self.last_error == None):
            self.last_error = error
            
        if (self.last_time == None):
            self.last_time = time.time()
            
        self.error_accum += error(time.time() - self.last_time)
        
        output += (self.kP * error)
        output += (self.kI * self.error_accum)
        output += (self.kD * ((error - self.last_error) / (time.time() - self.last_time)))
        
        #update persistant variables
        self.last_time = time.time()
        self.last_error = error
        
        return output #return power
import PID_controller

class PID_commander:
    def __init__(self):
        pass
            
        x_PID = PID_controller(1.0, 1.0, 1.0)        
        y_PID = PID_controller(2.0, 2.0, 2.0)
        z_PID = PID_controller(3.0, 3.0, 3.0)
        pitch_PID = PID_controller(4.0, 4.0, 4.0)
        roll_PID = PID_controller(5.0, 5.0, 5.0)
        yaw_PID = PID_controller(6.0, 6.0, 6.0)
        
    def calculate (self,
                setpointX : float, measurementX : float, velocityMeasureX : float,
                setpointY : float, measurementY : float, velocityMeasureY : float,
                setpointZ : float, measurementZ : float, velocityMeasureZ : float,
                setpointRoll : float, measurementRoll : float, velocityMeasureRoll : float,
                setpointPitch : float, measurementPitch : float, velocityMeasurePitch : float,
                setpointYaw : float, measurementYaw : float, velocityMeasureYaw : float,
                thrustX : float = None, VelocitySetX : float = None,
                thrustY : float = None, VelocitySetY : float = None,
                thrustZ : float = None, VelocitySetZ : float = None,
                thrustRoll : float = None, VelocitySetRoll : float = None,
                thrustPitch : float = None, VelocitySetPitch : float = None,
                thrustYaw : float = None, VelocitySetYaw : float = None
                ):
        
        if (thrustX != None):
            self.X_power = thrustX
        else:
            self.X_power = self.x_PID.calculate(setpointX, measurementX)
            
        if (thrustY != None):
            self.Y_power = thrustY
        else:
            self.Y_power = self.y_PID.calculate(setpointY, measurementY)
            
        if (Z_power != None):
            self.Z_power = Z_power
        else:
            self.Z_power = self.z_PID.calculate(setpointZ, measurementZ)
            
        if (Roll_power != None):
            self.Roll_power = Roll_power
        else:
            self.Roll_power = self.Roll_PID.calculate(setpointRoll, measurementRoll)
            
        if (Pitch_power != None):
            self.Pitch_power = Pitch_power
        else:
            self.Pitch_power = self.Pitch_PID.calculate(setpointPitch, measurementPitch)
            
        if (Yaw_power != None):
            self.Yaw_power = Yaw_power
        else:
            self.Yaw_power = self.yaw_PID.calculate(setpointYaw, measurementYaw)
    
        powers = [self.X_power, self.Y_power, self.Z_power, self.Roll_power, self.Pitch_power, self.Yaw_power]
        
        return powers
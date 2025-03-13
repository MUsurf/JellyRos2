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
        
        #x, y, z, roll, pitch, yaw
        self.PID_List = [x_PID, y_PID, z_PID, roll_PID, pitch_PID, yaw_PID]
        
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
                thrustYaw : float = None, VelocitySetYaw : float = None,
                
                xProperties : list, #set point, measurement, velocity measurement, thrust, velocity set
                yProperties: list,
                zProperties : list,
                rollProprerties : list,
                pitchProperties : list,
                yawProperties : list
                ):
        
        if (thrustX != None):
            self.thrustX = thrustX
        elif (velocitySetX != None):
            self.velocitySetX = VelocitySetX
        else:
            self.velocitySetX = self.PID_List[0].calculate(setpointX, measurementX)
            
        if (thrustY != None):
            self.thrustY = thrustY
        elif (velocitySetY != None):
            self.velocitySetY = VelocitySetY
        else:
            self.velocitySetY = self.y_PID.calculate(setpointY, measurementY)
            
        if (thrustZ != None):
            self.thrustZ = thrustZ
        elif (velocitySetZ != None):
            self.velocitySetZ = VelocitySetZ
        else:
            self.velocitySetZ = self.z_PID.calculate(setpointZ, measurementZ)
            
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
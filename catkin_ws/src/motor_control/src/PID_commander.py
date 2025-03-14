import PID_controller

class PID_commander:
    def __init__(self):            
        #x, y, z, roll, pitch, yaw
        self.PID_List = [
            PID_controller(1.0, 1.0, 1.0),        
            PID_controller(2.0, 2.0, 2.0),
            PID_controller(3.0, 3.0, 3.0),
            PID_controller(4.0, 4.0, 4.0),
            PID_controller(5.0, 5.0, 5.0),
            PID_controller(6.0, 6.0, 6.0)
            ]
        
    '''setpointX : float, measurementX : float, velocityMeasureX : float,
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
                thrustYaw : float = None, VelocitySetYaw : float = None,'''
        
    def calculate (self,
                #x, y, z, roll, pitch, yaw
                setPointList : list = [],
                measurementList : list = [],
                velocityMeasurementList : list = [None],
                thrustList : list = [None],
                velocitySetList : list = [None]
                ):
        
        for i in range(6):
            if (self.thrustList[i] != None):
                self.thrustList[i]= thrustList[i]
            elif (self.velocitySetList[i] != None):
                self.velocitySetList[i]= velocitySetList[i]
            else:
                thrustList[i] = self.PID_List[i].calculate(setPointList[i], measurementList[i])
        
        '''if (Yaw_power != None):
            self.Yaw_power = Yaw_power
        else:
            self.Yaw_power = self.yaw_PID.calculate(setpointYaw, measurementYaw)'''
    
        powers = [self.X_power, self.Y_power, self.Z_power, self.Roll_power, self.Pitch_power, self.Yaw_power]
        
        return powers
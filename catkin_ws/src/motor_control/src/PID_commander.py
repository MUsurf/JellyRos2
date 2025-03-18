from catkin_ws.src.motor_control.src.controllers import PIDController, FeedforwardController
class PID_commander:
    def __init__(self):            
        #x, y, z, roll, pitch, yaw
        self.positional_pid_controllers = [
            PIDController(1.0, 1.0, 1.0),        
            PIDController(2.0, 2.0, 2.0),
            PIDController(3.0, 3.0, 3.0),
            PIDController(4.0, 4.0, 4.0),
            PIDController(5.0, 5.0, 5.0),
            PIDController(6.0, 6.0, 6.0)
            ]
        self.velocity_pid_controllers = [
            PIDController(1.0, 1.0, 1.0),        
            PIDController(2.0, 2.0, 2.0),
            PIDController(3.0, 3.0, 3.0),
            PIDController(4.0, 4.0, 4.0),
            PIDController(5.0, 5.0, 5.0),
            PIDController(6.0, 6.0, 6.0)
        ]
        self.feedforward_controllers = [
            FeedforwardController(0.0, 0.0),
            FeedforwardController(0.0, 0.0),
            FeedforwardController(0.0, 0.0),
            FeedforwardController(0.0, 0.0),
            FeedforwardController(0.0, 0.0),
            FeedforwardController(0.0, 0.0),
        ]
        
    def calculate (self,
                #x, y, z, roll, pitch, yaw
                setPointList : list = [],
                measurementList : list = [],
                velocityMeasurementList : list = [None],
                thrustList : list = [None],
                velocitySetList : list = [None]
                ):
        
        """
        Notes: 
            -What is self.thrustList, self.velocitySetList, etc?
            -Why u guys got so many self.variables in here? As far as i know, the only thing that should need to be accessed
            via class variables is the controller lists
            -I changed the name of a file to controllers.py, changed the way you import it, and added it as one of the lists. I also
            added the velocity pid list.
        """
        
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
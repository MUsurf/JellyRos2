from catkin_ws.src.motor_control.src.controllers import PIDController, FeedforwardController
class PID_commander:
    def __init__(self):            
        #x, y, z, roll, pitch, yaw
        self.positional_pid_controllers = [
            PIDController(1.0, 1.0, 1.0),   #X      
            PIDController(2.0, 2.0, 2.0),   #Y
            PIDController(3.0, 3.0, 3.0),   #Z
            PIDController(4.0, 4.0, 4.0),   #ROLL
            PIDController(5.0, 5.0, 5.0),   #PITCH
            PIDController(6.0, 6.0, 6.0)    #YAW
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
                velocityMeasurementList : list = [],
                thrustList : list = [None],
                velocitySetPointList : list = [None]
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
            if (thrustList[i] != None):
                thrustList[i]= thrustList[i]
            elif (velocitySetPointList[i] != None):
                velocitySetPointList[i]= velocitySetPointList[i]
            else:
                velocitySetPointList[i] = self.positional_pid_controllers[i].calculate(setPointList[i], measurementList[i])
                
                
                
        
        '''if (Yaw_power != None):
            self.Yaw_power = Yaw_power
        else:
            self.Yaw_power = self.yaw_PID.calculate(setpointYaw, measurementYaw)'''
        
        return thrustList
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
                positionSetPointList : list = [], #Input desired positions
                poisitionMeasurementList : list = [], #Input current positional measurements
                velocityMeasurementList : list = [], #Input current velocity measurements
                thrustList : list = [None], #Final, returned list of thrust power output
                velocitySetPointList : list = [None] #Velocity desired measurement. Input or filled by positional PIDs
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
            #Check if thrust powers are given
            if (thrustList[i] != None):
                return thrustList
            #Check if velocity set points are not given
            elif (velocitySetPointList[i] == None):
                #Call positional PIDs to create velocity set points if they are not given
                velocitySetPointList[i] = self.positional_pid_controllers[i].calculate(positionSetPointList[i], poisitionMeasurementList[i])
            #Call velocity PIDs to create end velocity list
            PIDvelocityList = self.velocity_pid_controllers[i].calculate(velocitySetPointList[i], velocityMeasurementList[i])
            #Call feed forward PIDs
            feedForwardVelocityList = self.feedforward_controllers[i].calculate(velocitySetPointList)
        
            for j in range(6):
                #Fill thrust list by summation of velocity PID and feed forward outputs
                thrustList[j] = PIDvelocityList[j] + feedForwardVelocityList[i]
        
        return thrustList
    
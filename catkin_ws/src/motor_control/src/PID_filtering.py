import PID_controller
class PID_filtering:
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
            if (X_power != None):
                X_power = X_power
            else:
                X_power = calculate(setpointX, measurementX)
            if (Y_power != None):
                Y_power = Y_power
            else:
                Y_power = calculate(setpointY, measurementY)
            if (Z_power != None):
                Z_power = Z_power
            else:
                Z_power = calculate(setpointZ, measurementZ)
            if (Roll_power != None):
                Roll_power = Roll_power
            else:
                Roll_power = calculate(setpointRoll, measurementRoll)
            if (Pitch_power != None):
                Pitch_power = Pitch_power
            else:
                Pitch_power = calculate(setpointPitch, measurementPitch)
            if (Yaw_power != None):
                Yaw_power = Yaw_power
            else:
                Yaw_power = calculate(setpointYaw, measurementYaw)
            # defining a decorator  
            def controller_wrapper(func):  
                
                # inner1 is a Wrapper function in   
                # which the argument is called  
                def inner1():
                    pass
                # inner function can access the outer local  
                # functions like in this case "func" 
                
                    # calling the actual function now  
                    # inside the wrapper function.  
                    func()
                    
                return inner1

                
            def Controller():
                pass
            Controller = controller_wrapper(Controller)
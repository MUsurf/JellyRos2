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
                self.X_power = X_power
            else:
                self.X_power = calculate(setpointX, measurementX)
            if (Y_power != None):
                self.Y_power = Y_power
            else:
                self.Y_power = calculate(setpointY, measurementY)
            if (Z_power != None):
                self.Z_power = Z_power
            else:
                self.Z_power = calculate(setpointZ, measurementZ)
            if (Roll_power != None):
                self.Roll_power = Roll_power
            else:
                self.Roll_power = calculate(setpointRoll, measurementRoll)
            if (Pitch_power != None):
                self.Pitch_power = Pitch_power
            else:
                self.Pitch_power = calculate(setpointPitch, measurementPitch)
            if (Yaw_power != None):
                self.Yaw_power = Yaw_power
            else:
                self.Yaw_power = calculate(setpointYaw, measurementYaw)
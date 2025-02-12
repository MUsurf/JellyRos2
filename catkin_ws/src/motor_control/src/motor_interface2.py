# Begin typing imports
from typing import List
# End typing imports

#MAX_POSITIVE?
#MAX_NEGATIVE?

class motor_interface():
    def __init__(self):
        #STUFF?
        x = 1 

    # Function to convert inputs for desired x, y, yaw into powers for motors 1, 2, 3, 4
    def horz_power(self, x : float, y : float, yaw : float) -> list:
        # Motors 1, 2, 3, 4 (CCW starting from top right motors as seen from above)
        powers = [0, 0, 0, 0]
        # Define lists of power in single direction
        powers_x = [x, x, x, x]
        powers_y = [-y, y, -y, y]
        powers_yaw = [yaw, -yaw, -yaw, yaw]
        
        #Sum powers into single list
        for i in range(len(powers)):
            powers[i] = powers_x[i] + powers_y[i] + powers_yaw[i]
            
        return powers
    
    def vert_power(self, roll: float, pitch: float, z: float) -> list:
        #list is read [top right, top left, bottom left, bottom right]
        powers = [0,0,0,0]

        powers[0] = z + roll + pitch
        powers[1] = z - roll + pitch
        powers[2] = z - roll - pitch
        powers[3] = z + roll - pitch

        return powers
    
    
    def hortical_pow(self, x : float, y : float, yaw : float, roll: float, pitch: float, z: float) -> list:
        powers = [0, 0, 0, 0, 0, 0, 0, 0]
        
        powers_vert = self.vert_power(roll, pitch, z)
        powers_horz = self.horz_power(x, y, z)
        
        # Assign first 4 motor powers (horizontal)
        for i in range(4):
            powers[i] = powers_horz[i]
            
        # Assign second 4 motors (vertical)
        for i in range(4):
            powers[i+3] = powers_vert[i]
            
        # Sum powers into single list
        for i in range(len(powers)):
            if (powers[i] > 0):
                powers[i] = self.power_scale(powers[i]) # Negative power output is less than positive; compensate by lowering pos.
        
        return powers
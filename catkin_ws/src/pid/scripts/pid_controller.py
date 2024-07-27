# Begin Imports
import time
from pid_driver import Pid_object

import rospy
from std_msgs.msg import Float32MultiArray
# End Imports

#! make pids able to subscribe 

class PID_controller():
    def __init__(self, ttw: int) -> None:
        """This does not setup any pid controllers that is to be done at a later step

        Parameters
        ----------
        ttw : int
            time to wait until next step
        """        

        self.pid_objects: list[Pid_object] = []

        self.current_values: list[float] = []

        self.time_counter = time.time()
        self.wait_time: int = ttw

        # Ros things
        self.publishers = []

    def init_pid(self, error: float, integral: float, prop: float, derivative: float, bias: float, set_point: float, current_value: float) -> int:
        """This starts a pid controller with provided settings

        This starts a pid instance with the settings provided and returns the id for future refrence

        Parameters
        ----------
        error : float
            The amount of distance between 'set_point' and 'current_value'
        integral : float
            The integral component
        prop : float
            The proportional component
        derivative : float
            The derivitive component
        bias : float
            The bias drive
        set_point : float
            The target value of the PID
        current_value : float
            The value to start the system

        Returns
        -------
        int
            Id of pid added
        """        

        pid_id = len(self.pid_objects)
        self.pid_objects.append(Pid_object(error, integral, prop, derivative, bias, set_point, current_value))
        self.current_values.append(current_value)
        return pid_id
    
    def init_publisher(self, topic_name: str) -> int:
        publisher_id = len(self.publishers)
        pub = rospy.Publisher(topic_name, Float32MultiArray, queue_size=10)
        self.publishers.append(pub)
        return publisher_id


    def __pid_step(self, pid_object: Pid_object, current_value: float) -> float:
        return pid_object.Update(current_value)

    def step_all(self, current_values: "list[float]") -> None:
        """Update all PID objects

        WARNING probably should not be used out of class

        Parameters
        ----------
        current_values : list[float]
            values for the PIDs
        """
        assert (len(current_values) == len(self.pid_objects))

        for counter in range(len(current_values)):
            self.current_values[counter] = self.__pid_step(self.pid_objects[counter], current_values[counter])

    def step_one(self, current_value: float, pid_id: int) -> None:
        """Update one PID object

        WARNING probably should not be used out of class

        Parameters
        ----------
        current_value : float
            value for PID being updated
        pid_id : int
            pid to update
        """
        self.__pid_step(self.pid_objects[pid_id], current_value)

    def ros_update_reading(self, data, args) -> None:
        """Function to give ros for callback

        Parameters
        ----------
        data : _type_
            data from ros
        args : tuple(int)
            contains index for pid to change
        """
        self.current_values[args[0]] = data.data


    def sm_update(self, setpoint:float, index:int) -> None:
        """Method to be called by state machine to update target parameters

        Parameters
        ----------
        setpoint : float
            target value for pid
        index : int
            pid to change
        """

        self.pid_objects[index].Update_setpoint(setpoint)
    
    def spin(self) -> None:
        """ros runner function"""

        rate = rospy.Rate(10)  # Set a rate for publishing (10 Hz)

        while not rospy.is_shutdown():
            current_time = time.time()
            if (current_time > (self.wait_time + self.time_counter)):
                self.time_counter = current_time
                self.step_all(self.current_values)
                rospy.loginfo(self.current_values)
                
                # Prepare the message to publish
                msg = Float32MultiArray()
                msg.data = self.current_values
                
                # Publish the message to the motor command topics
                for publisher in self.publishers:
                    publisher.publish(msg)

                rate.sleep()
        
    def get_pid_out(self, pid_id):
        """should only be used shortly after updating pid

        Parameters
        ----------
        pid_id : int
            pid of intrest

        Returns
        -------
        float
            current state of pid driving
        """
        return self.current_values[pid_id]





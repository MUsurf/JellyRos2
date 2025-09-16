#!/usr/bin/env python3

'''
ROS
---

node:
----
        - motor_commander

Publishes:
---------
        - motor_command

Subscribes:
----------

'''


"""

! This is just a test driver function not used in comp

"""



# BEGIN IMPORT
import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
# END IMPORT

from typing import List


class MotorCommander(Node):
    def __init__(self):
        super().__init__('motor_commander')
        self.publisher = self.create_publisher(Int32MultiArray, 'motor_command', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        
        self.num_motors = 8
        self.wait_time : float = 30
        self.sequence_time : float = 15
        
        self.start_time : float = time.time()
        self.first : bool = True
        
        self.motor_sequences : List[int] = [
            [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
            [0.0, 0.0, 0.0, 0.0, 30.0, 30.0, 30.0, 30.0],
            [30.0, 30.0, 30.0, 30.0, 0.0, 0.0, 0.0, 0.0]
        ]
        self.low: List[int] = [0 for _ in range(self.num_motors)]
        self.sequence_counter = 0
        self.activated = False
        
        self.get_logger().info('MotorCommander Node Created')
    
    def timer_callback(self):
        if self.first:
            self.publish_motor_data(self.low)
            
            self.first = False
            self.activated = False
            self.start_time = time.time()
            
        elif time.time() - self.start_time >= (self.sequence_time if self.activated else self.wait_time):
            self.publish_motor_data(self.low if self.activated else self.motor_sequences[self.sequence_counter%len(self.motor_sequences)])
            
            self.motor_sequences += 1
            self.activated = not self.activated
            self.start_time = time.time()
        
    def publish_motor_data(self, data : list):
        msg = Int32MultiArray()
        msg.data = data
        self.get_logger().info(f'Publishing: {msg.data}')
        self.publisher.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    node = MotorCommander()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down MotorCommander")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
#!/usr/bin/env python

'''
ROS 

node: depth_node
Publishes:
Subscribes:
        - rov/ms5837

Maintainer: Henry Bloch
'''

import rospy

class depth_smoother():




def depth_callback(data):
    rospy.loginfo(data.tempF)

def depth_setup():
    """Creates ROS components for depth calibration and smoothing nodes"""
    
    # Setup Node
    rospy.init_node("depth_node", anonymous=True)
    # Setup Subscriber
    rospy.Subscriber("rov/ms5837", ms5837_data, depth_callback)
    # Keep the node running
    # rospy.Publisher("clean_depth", ms5837_data, queue_size=10)
    rospy.spin()

def depth_ros_runner():
    rospy.loginfo(data.tempF)
    pub.publish(data="none")


if __name__ == '__main__':
	try:
        depth_setup()
    except KeyboardInterrupt:
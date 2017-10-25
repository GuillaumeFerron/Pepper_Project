#!/usr/bin/env python

import rospy	# Ros module for python
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import *

obstacle = {5.0, 5.0}

def getPose(data):
	print(data.data)

def obstacle_avoidance():
	# Publish the 'cmd_vel' topic using Twist messages
	vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	pose = rospy.Subscriber('/turtle1/pose', String, getPose)
	# Node name
	rospy.init_node('pepper_master')
	rate = rospy.Rate(10) # 10hz
	joy = Twist()
	joy.linear.x = 1.0 # joystick comand
	calc = Twist()
	while not rospy.is_shutdown():
		# Simulate an obstacle in the middle
		theta = 0
		joyx = joy.linear.x	
		# publish the comands on the topic
		vel.publish(joy)
		rate.sleep()
	
if __name__ == '__main__':
	obstacle_avoidance()


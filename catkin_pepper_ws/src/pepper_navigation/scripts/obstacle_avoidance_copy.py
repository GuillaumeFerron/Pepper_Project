#!/usr/bin/env python

import rospy	# Ros module for python
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import *


vel = None
laser_twist = Twist()
tw = Twist()
cmd_twist = Twist()

def get_joy(data):
	global laser_twist
	global vel
	global cmd_twist
	if(data.linear.x==0.0 and data.linear.y==0.0 and data.angular.z==0.0):
		cmd_twist.linear.x=0.0
		cmd_twist.linear.y=0.0
		cmd_twist.angular.z=0.0
	else:
		cmd_twist.linear.x=max(min(data.linear.x+laser_twist.linear.x,1.0),-1.0)*0.5
		cmd_twist.linear.y=max(min(data.linear.y+laser_twist.linear.y,1.0),-1.0)*0.5
		#if data.angular.z==0.0:
		#	cmd_twist.angular.z=max(min(laser_twist.angular.z,1.0),-1.0)
		#else:
		cmd_twist.angular.z=data.angular.z

	cmd_twist.linear.z=0.0
	cmd_twist.angular.x=0.0
	cmd_twist.angular.y=0.0
	

	vel.publish(cmd_twist)
	print("")
	print("JOY:")
	print(data)
	print("LASERS:")
	print(laser_twist)
	print("COMMANDE:")
	print(cmd_twist)


def get_lasers(data):
	global tw	
	tw.linear.x=0.0
	tw.linear.y=0.0
	tw.linear.z=0.0
	tw.angular.x=0.0
	tw.angular.y=0.0
	tw.angular.z=0.0
	nbobstacles=0.0
	for i in range(61):
		angle=data.angle_min+i*data.angle_increment
		if(data.ranges[i]>0.0 and data.ranges[i]<1.0):
			nbobstacles=nbobstacles+1.0
			tw.linear.x=tw.linear.x-cos(angle)/(data.ranges[i])
			tw.linear.y=tw.linear.y-sin(angle)/(data.ranges[i])
			tw.angular.z=tw.angular.z-angle/(data.ranges[i])
			if data.ranges[i]<1.0:
				print("- Obstacle:")
				print(angle)
	if nbobstacles != 0:
		tw.linear.x=tw.linear.x/(nbobstacles*5.0)
		tw.linear.y=tw.linear.y/(nbobstacles*5.0)
		tw.angular.z=tw.angular.z/(nbobstacles*5.0)
	global laser_twist
	laser_twist = tw	

def obstacle_avoidance():
	# Publish the 'cmd_vel' topic using Twist messages
	global vel	
	vel = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
	# Listen to the lasers and joy
	lasers = rospy.Subscriber("/pepper_robot/laser", LaserScan, get_lasers)
	joy_cmd = rospy.Subscriber("joy_twist", Twist, get_joy) #joy_twist

	# Node name
	rospy.init_node('pepper_master')
#	rate = rospy.Rate(10) # 10hz
#	cmd = Twist()
#	cmd.linear.x = 1.0 # joystick comand
#	calc = Twist()
#	while not rospy.is_shutdown():
#		
#		# publish the comands on the topic
#		vel.publish(cmd)
#		rate.sleep()

	rospy.spin()
	
if __name__ == '__main__':
	obstacle_avoidance()


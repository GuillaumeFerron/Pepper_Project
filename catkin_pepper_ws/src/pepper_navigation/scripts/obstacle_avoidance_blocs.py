#!/usr/bin/env python

import rospy  # Ros module for python
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import *
import numpy

vel = None
laser_twist = Twist()
tw = Twist()
cmd_twist = Twist()


def get_joy(data):
    global laser_twist
    global vel
    global cmd_twist

    delta = 0.3  # minimize repulsion vector
    if data.linear.x == 0.0 and data.linear.y == 0.0:
        cmd_twist.linear.x = 0.0
        cmd_twist.linear.y = 0.0
    else:
		
		norme_laser=sqrt(laser_twist.linear.x*laser_twist.linear.x+laser_twist.linear.y*laser_twist.linear.y)
        norme_laser=min(1,norme_laser)
        
        cmd_twist.linear.x = data.linear.x/2.0 + delta * laser_twist.linear.x/norme_laser
        cmd_twist.linear.y = data.linear.y/2.0 + delta * laser_twist.linear.y/norme_laser
        
        """i =1
        #check if V' is opposite on x and y to V:
        while(cmd_twist.linear.x * data.linear.x + cmd_twist.linear.y*data.linear.y <= 0):
            print("in while")
            cmd_twist.linear.x=max(min(data.linear.x+pow(delta,i)*laser_twist.linear.x,1.0),-1.0)
            cmd_twist.linear.y=max(min(data.linear.y+pow(delta,i)*laser_twist.linear.y,1.0),-1.0)
            i=+1
        #if data.angular.z==0.0:
        #	cmd_twist.angular.z=max(min(laser_twist.angular.z,1.0),-1.0)
        #else:
        print("out of while")"""
    cmd_twist.angular.z = data.angular.z

    cmd_twist.linear.z = 0.0
    cmd_twist.angular.x = 0.0
    cmd_twist.angular.y = 0.0

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
    tw.linear.x = 0.0
    tw.linear.y = 0.0
    tw.linear.z = 0.0
    tw.angular.x = 0.0
    tw.angular.y = 0.0
    tw.angular.z = 0.0
    nbobstacles = 0.0
    
    for i in range(61):  # 61 points on laser 3*15 + 2*8 points on dead angles
        angle = data.angle_min + i * data.angle_increment
        if 0.0 < data.ranges[i] < 1:
            
            if(data.ranges[
            nbobstacles = nbobstacles + 1.0
            # - for repulsive vector
            # the x value of the current repulsive vector is d*cos(angle)
            # since we want the 1/d*d*d * OA
            # we add d*cos(angle)/d*d*d = cos(angle)/d*d
            tw.linear.x = tw.linear.x - cos(angle) / (data.ranges[i] * data.ranges[i])
            tw.linear.y = tw.linear.y - sin(angle) / (data.ranges[i] * data.ranges[i])

            # tw.angular.z= tw.angular.z-angle/(data.ranges[i])
            print("- Obstacle:")
            print(angle, tw.linear.x, tw.linear.y)
    if nbobstacles != 0:  # normalization
        tw.linear.x = tw.linear.x / nbobstacles
        tw.linear.y = tw.linear.y / nbobstacles
    # tw.angular.z=tw.angular.z/(nbobstacles)
    global laser_twist
    laser_twist = tw
    print("lt : ", tw.linear.x, tw.linear.y)


def obstacle_avoidance():
    # Publish the 'cmd_vel' topic using Twist messages
    global vel
    rospy.init_node('pepper_master')
    vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # Listen to the lasers and joy
    lasers = rospy.Subscriber("/pepper_robot/laser", LaserScan, get_lasers)
    joy_cmd = rospy.Subscriber("joy_twist", Twist, get_joy)  # joy_twist

    # Node name

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

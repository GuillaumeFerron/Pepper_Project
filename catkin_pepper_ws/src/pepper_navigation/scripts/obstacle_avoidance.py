#!/usr/bin/env python

import rospy  # Ros module for python
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Range
from math import *
import numpy

vel = None

""" Pepper metaparameters """
DETECTION_DISTANCE = 2
CRITICAL_DISTANCE = 0.5
delta = 0.3  # minimize repulsion vector
EMERGENCY_STOP_FRONT = 0
EMERGENCY_STOP_BACK = 0

""" Twists declarations """
laser_twist = Twist()
tw = Twist()
cmd_twist = Twist()
norme_max = 1.0

def get_joy(data):
    global laser_twist
    global vel
    global cmd_twist
    global norme_max #test1
    global delta
    global EMERGENCY_STOP_FRONT
    global EMERGENCY_STOP_BACK
    if (data.linear.x == 0.0 and data.linear.y == 0.0):
        cmd_twist.linear.x = 0.0
        cmd_twist.linear.y = 0.0
    
    elif (data.linear.x > 0 and EMERGENCY_STOP_FRONT == 1) or (data.linear.x < 0 and EMERGENCY_STOP_BACK == 1):
        cmd_twist.linear.x = 0.0

    else:
        norme_laser=sqrt(laser_twist.linear.x*laser_twist.linear.x+laser_twist.linear.y*laser_twist.linear.y)
        norme_max=max(min(1,norme_laser),norme_max) 
        
        cmd_twist.linear.x = data.linear.x + delta * laser_twist.linear.x/norme_max
        cmd_twist.linear.y = data.linear.y + delta * laser_twist.linear.y/norme_max


#        norme=max(1,sqrt(cmd_twist.linear.x * cmd_twist.linear.x + cmd_twist.linear.y * cmd_twist.linear.y))
        
#        cmd_twist.linear.x = cmd_twist.linear.x / norme
#        cmd_twist.linear.y = cmd_twist.linear.y / norme

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
    print("EMERGENCY_STOP_FRONT:")
    print(EMERGENCY_STOP_FRONT)
    print("EMERGENCY_STOP_BACK:")
    print(EMERGENCY_STOP_BACK)    


def get_lasers(data):
    global tw
    tw.linear.x = 0.0
    tw.linear.y = 0.0
    tw.linear.z = 0.0
    tw.angular.x = 0.0
    tw.angular.y = 0.0
    tw.angular.z = 0.0
    nbobstacles = 0.0
    
	global joy_twist
    # Calcul de l'angle du joy
    if joy_twist.linear.x == 0.0:
        angle_joy = 0.0
    else:
		angle_joy = atan(joy_twist.linear.y/joy_twist.linear.x)
    
    
    
    for i in range(61):  # 61 points on laser 3*15 + 2*8 points on dead angles
        angle = data.angle_min + i * data.angle_increment
        coeff_angle=0.5
        if angle_joy-1.0 < angle < angle_joy+1.0:
			coeff_angle=1.5
        if 0.0 < data.ranges[i] < DETECTION_DISTANCE:
            nbobstacles = nbobstacles + 1.0
            # - for repulsive vector
            # the x value of the current repulsive vector is d*cos(angle)
            # since we want the 1/d*d*d * OA
            # we add d*cos(angle)/d*d*d = cos(angle)/d*d
            tw.linear.x = tw.linear.x - coeff_angle * cos(angle) / (data.ranges[i] * data.ranges[i])
            tw.linear.y = tw.linear.y - coeff_angle * sin(angle) / (data.ranges[i] * data.ranges[i])

            # tw.angular.z= tw.angular.z-angle/(data.ranges[i])
            # print("- Obstacle:")
            # print(angle, tw.linear.x, tw.linear.y)
    if nbobstacles != 0:  # normalization
        tw.linear.x = tw.linear.x / nbobstacles
        tw.linear.y = tw.linear.y / nbobstacles
    # tw.angular.z=tw.angular.z/(nbobstacles)
    global laser_twist
    laser_twist = tw
    # print("lt : ", tw.linear.x, tw.linear.y)


def get_sonar_front(data):
    global EMERGENCY_STOP_FRONT
    EMERGENCY_STOP_FRONT = 0
    obstacleDist = data.range
    
    if obstacleDist < CRITICAL_DISTANCE:
        EMERGENCY_STOP_FRONT = 1
    else:
        EMERGENCY_STOP_FRONT = 0

def get_sonar_back(data):
    global EMERGENCY_STOP_BACK
    EMERGENCY_STOP_BACK = 0
    obstacleDist = data.range
    
    if obstacleDist < CRITICAL_DISTANCE:
        EMERGENCY_STOP_BACK = 1
    else:
        EMERGENCY_STOP_BACK = 0
    

def obstacle_avoidance():
    # Publish the 'cmd_vel' topic using Twist messages
    global vel
    rospy.init_node('pepper_master')
    vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # Listen to the lasers and joy
    lasers = rospy.Subscriber("/pepper_robot/laser", LaserScan, get_lasers)
    sonar_front = rospy.Subscriber("/pepper_robot/sonar/front", Range, get_sonar_front)
    sonar_back = rospy.Subscriber("/pepper_robot/sonar/back", Range, get_sonar_back)
    joy_cmd = rospy.Subscriber("joy_twist", Twist, get_joy)  # joy_twist

    rospy.spin()


if __name__ == '__main__':
    obstacle_avoidance()

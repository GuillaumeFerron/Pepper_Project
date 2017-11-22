#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""
import qi
import time
import sys
import argparse
import rospy
from geometry_msgs.msg import Twist
from math import *

vel=None



""" Pepper metaparameters """
DIST_MIN = 0.5
ANGLE_MAX = 0.09
X_VELOCITY = 0.5
Z_ANGULAR_VELOCITY = 0.3

""" Twists declarations """
cmd_twist = Twist()



class PersonDetection(object):
	"""
	A simple class to react to face detection events.
	"""

	def __init__(self, app):
		"""
		Initialisation of qi framework and event detection.
		"""
		super(PersonDetection, self).__init__()
	
		app.start()
		session = app.session
		# Get the service ALMemory.
		self.memory = session.service("ALMemory")
		# Connect the event callback.
		self.detected_subscriber = self.memory.subscriber("PeoplePerception/PeopleDetected")
		self.detected_subscriber.signal.connect(self.on_human_detected)
		# Get the services ALTextToSpeech and ALFaceDetection.
		self.tts = session.service("ALTextToSpeech")
		self.detected = session.service("ALPeoplePerception")
		self.detected.subscribe("PersonDetection")
		self.got_face = False
	
	
	def on_human_detected(self,value):
		print("detected  human")
		global cmd_twist
		global vel
		if value == []:  # empty value when the face disappears
		    print("no people detected")
		    #self.tts.say("je ne te vois plus")
		else:
		    
		    # First Field = TimeStamp.
		    timeStamp = value[0]
		    print "TimeStamp is: " + str(timeStamp[0])

		    # Second Field = array of face_Info's.
		    personDataList = value[1]
		    for j in range( len(personDataList) ):
			personData = personDataList[j]

		    	person_id = personData[0]
		    	person_dist = personData[1]
			person_pitch = personData[2]
			person_yaw = personData[3]
			#self.tts.say("tu es "+str(person_id))
		   	print "Person id :  %d - person_dist %.3f " % (person_id, person_dist)
			print "pitch" + str(person_pitch)+ "yaw" +str(person_yaw)
			person_shirt = self.memory.getData("PeoplePerception/Person/"+str(person_id)+"/ShirtColor")
			person_face = self.memory.getData("PeoplePerception/Person/"+str(person_id)+"/IsFaceDetected")
			print("shirt color : ", person_shirt, " face : ", str(person_face))
			global vel
			global cmd_twist
			if person_yaw < -ANGLE_MAX :
				cmd_twist.angular.z = - Z_ANGULAR_VELOCITY
			elif person_yaw > ANGLE_MAX :
				cmd_twist.angular.z = Z_ANGULAR_VELOCITY
			if person_dist > DIST_MIN:
				cmd_twist.linear.x =X_VELOCITY
				vel.publish(cmd_twist)
			cmd_twist.linear.x=0.0
			cmd_twist.angular.z=0.0 
	

	def run(self):
		"""
		Loop on, wait for events until manual interruption.
		"""
		print "Starting PersonDetection"

	    	
		try:
		    while True:
		        time.sleep(1)
		except KeyboardInterrupt:
		    print "Interrupted by user, stopping PersonDetection"
		    self.detected.unsubscribe("PersonDetection")
		    #stop
		    sys.exit(0)
		
		   

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["PersonDetection", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    rospy.init_node('pepper_face_master')
    vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    person_detec =  PersonDetection(app)
    person_detec.run()
   
	

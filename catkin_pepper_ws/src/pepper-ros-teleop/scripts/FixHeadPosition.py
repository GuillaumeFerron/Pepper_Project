
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use setExternalCollisionProtectionEnabled Method"""

import qi
import argparse
import sys
import time


def main(session):
    """
    This example uses the setExternalCollisionProtectionEnabled method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")
    memory_service = session.service("ALMemory")
    fractionMaxSpeed = 0.5
    motion_service.setStiffnesses("HEAD", 1.0)
    motion_service.setStiffnesses("TORSO", 1.0)
    error=0.1
    isEnd=False

    try:
        while isEnd ==False:
            headYawPos = memory_service.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value")
            headPitchPos = memory_service.getData("Device/SubDeviceList/HeadPitch/Position/Sensor/Value")
            print("headYawPos:"+str(headYawPos)+",headPitchPos:"+str(headPitchPos))
            if abs(headPitchPos)>error or abs(headYawPos)>error:
                motion_service.setAngles("HeadYaw", 0.0, fractionMaxSpeed)
                motion_service.setAngles("HeadPitch", 0.0, fractionMaxSpeed)
                print("update head")

            time.sleep(0.1)
    finally:
        isEnd = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)

#*****************************#
#   ROBOT SIMULATION SCRIPT   #
#*****************************#

from morse.builder import *
import os

robot = ATRV()

camera = VideoCamera()
camera.translate(x=0.2, z=0.9)
camera.properties(cam_far=5000,cam_near=0.001)
robot.append(camera)

keyboard = Keyboard()
robot.append(keyboard)

blendfile = os.getcwd() + "/office_2016-07-07_00-25-07"
env = Environment(blendfile)
camera.add_service('yarp')
camera.add_stream('yarp')
keyboard.add_service('yarp')

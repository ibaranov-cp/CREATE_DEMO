#!/usr/bin/env python

import rospy
import sys
import time

from sensor_msgs.msg import JointState


def set_angles(pan, tilt):
    pub = rospy.Publisher("cmd", JointState)
    time.sleep(0.5)

    js = JointState()
    js.name = [ "ptu_pan", "ptu_tilt" ]
    js.velocity = [ 0.6, 0.6 ]
    js.position = [ pan, tilt ]
    pub.publish(js)
	
if __name__ == '__main__':
    rospy.init_node('ptu_cmd_angles')
    set_angles(
            float(sys.argv[1]),
            float(sys.argv[2]))

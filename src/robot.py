#!/usr/bin/env python

#Takes in /tf oculus frame, and drives ptu

import rospy
import sys
import time
import tf
import math
import geometry_msgs.msg
from sensor_msgs.msg import JointState
from tf.transformations import euler_from_quaternion

#roll = euler[0]
#pitch = euler[1]
#yaw = euler[2]

pan_store = -10
tilt_store = -10

def demo():
    global js
    global pub
    pub = rospy.Publisher("/ptu/cmd", JointState, queue_size=1)
    time.sleep(0.5)
    js = JointState()
    js.name = [ "ptu_pan", "ptu_tilt" ]
    rospy.init_node('robot',anonymous=True)
    listener = tf.TransformListener()

    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/base_link', '/oculus', rospy.Time(0))
            euler = tf.transformations.euler_from_quaternion(rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        set_angles(euler[2],-euler[1])
        rate.sleep()


def set_angles(pan, tilt):
    global pan_store
    global tilt_store

    rospy.loginfo(math.fabs(pan - pan_store))
    js.velocity = [ 2.5, 2.5 ]
    js.position = [ pan, tilt ]

    if ((math.fabs(pan - pan_store) >= 0.02) or (math.fabs(tilt - tilt_store) >= 0.02)):
        pub.publish(js)

    pan_store = pan
    tilt_store = tilt


if __name__ == '__main__':
    try:
        demo()
    except rospy.ROSInterruptException:
        pass

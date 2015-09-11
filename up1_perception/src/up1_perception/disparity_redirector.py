#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from stereo_msgs.msg import DisparityImage


# Exposes the Image attribute within DisparityImage and re-publishes it to
# /stereo/disparity/image
class DisparityRedirector(object):
    def __init__(self):
        rospy.init_node('disparity_redirector', anonymous=True)

        self.pub = rospy.Publisher('/stereo/disparity/image', Image, queue_size=10)
        rospy.Subscriber("/stereo/disparity", DisparityImage, self.callback)

        rospy.spin()

    def callback(self, disparity_image):
        self.pub.publish(disparity_image.image)

if __name__ == '__main__':
    DisparityRedirector()

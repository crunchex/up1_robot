import rospy
import cv2
from cv_bridge import CvBridge
from cmvision.msg import Blobs


class Vision:
    def __init__(self):
        self.bridge = CvBridge()
    
    def draw_rect(self, blob, image_cv, image_pub):
        x = blob.x
        y = blob.y
        h = blob.top-blob.bottom
        w = blob.right-blob.left
        cv2.rectangle(image_cv, (x-w/2, y-h/2), (x+w/2, y+h/2), (0, 255, 0), 2)
        image_pub.publish(self.bridge.cv2_to_imgmsg(image_cv, "bgr8"))
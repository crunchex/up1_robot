#!/usr/bin/env python
import rospy
from cmvision.msg import Blobs
from sensor_msgs.msg import Image
import up1_perception.vision as up1_vision

class object_detection():
    def __init__(self):
        rospy.init_node('object_detection', anonymous=True)
        self.vision = up1_vision.Vision()
        
        
        rospy.Subscriber('/stereo/left/image_raw', Image, self.camera_callback)
        self.image_pub = rospy.Publisher("image_object_recognition_square",Image, queue_size=5)
        
        self.hasCameraFrame = False

        while not self.hasCameraFrame:
            print 'waiting on camera info.'
            rospy.sleep(0.5)
        
        rospy.Subscriber('blobs', Blobs, self.blob_callback)
        rospy.spin()
    
    def camera_callback(self, image):
        self.hasCameraFrame = True
        self.image_cv = self.vision.bridge.imgmsg_to_cv2(image, 'bgr8')
    
    def blob_callback(self, blobs):
        for blob in blobs.blobs:
                if blob.name == 'Yellow_Cube':
                    print 'Yellow_Cube: x = ' + str(blob.x) + ' y = ' + str(blob.y)
                    self.vision.draw_rect(blob, self.image_cv, self.image_pub)
                elif blob.name == 'Green_Cube':
                    print 'Green_Cube: x = ' + str(blob.x) + ' y = ' + str(blob.y)
                    self.vision.draw_rect(blob, self.image_cv, self.image_pub)
                elif blob.name == 'Blue_Cube':
                    print 'Blue_Cube: x = ' + str(blob.x) + ' y = ' + str(blob.y)
                    self.vision.draw_rect(blob, self.image_cv, self.image_pub)
                elif blob.name == 'Pink_Cube':
                    print 'Pink_Cube: x = ' + str(blob.x) + ' y = ' + str(blob.y)
                    self.vision.draw_rect(blob, self.image_cv, self.image_pub)

if __name__ == '__main__':
    object_detection()
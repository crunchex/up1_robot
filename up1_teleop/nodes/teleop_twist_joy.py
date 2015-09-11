#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class TeleopTwistJoy():
    def __init__(self):
        self.msg = """
        ***************************************************
        *                                                 *
        * Press 'X' button to enable wheels.              *
        * Use left analog stick to drive.                 *
        *                                                 *
        ***************************************************
        """
        
        rospy.init_node('teleop_twist_joy')
        
        # ros params
        self.axis_linear = rospy.get_param('axis_linear', 1)
        self.scale_linear = rospy.get_param('scale_linear', 0.7)
        self.scale_linear_turbo = rospy.get_param('scale_linear_turbo', 1.5)
        
        self.axis_angular = rospy.get_param('axis_angular', 0)
        self.scale_angular = rospy.get_param('scale_angular', 0.4)
        
        self.enable_button = rospy.get_param('enable_button', 2)
        self.enable_turbo_button = rospy.get_param('enable_turbo_button', 5)
        
        self.sent_disable_msg = False
        
        rospy.Subscriber('joy', Joy, self.callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        
        print self.msg
        
        rospy.spin()


    def callback(self, joy_msg):
        twist = Twist()

        if joy_msg.buttons[self.enable_turbo_button]:
            twist.linear.x = joy_msg.axes[self.axis_linear] * self.scale_linear_turbo
            twist.angular.z = joy_msg.axes[self.axis_angular] * self.scale_angular
            self.cmd_vel_pub.publish(twist)
            self.sent_disable_msg = False

        elif joy_msg.buttons[self.enable_button]:
            twist.linear.x = joy_msg.axes[self.axis_linear] * self.scale_linear
            twist.angular.z = joy_msg.axes[self.axis_angular] * self.scale_angular
            self.cmd_vel_pub.publish(twist)
            self.sent_disable_msg = False

        elif self.sent_disable_msg == False:
            # When enable button is released, immediately send a single no-motion command
            # in order to stop the robot.
            self.cmd_vel_pub.publish(twist)
            self.sent_disable_msg = True

if __name__ == '__main__':
    teleopTwistJoy = TeleopTwistJoy()

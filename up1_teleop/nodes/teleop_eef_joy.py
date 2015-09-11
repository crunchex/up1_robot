#!/usr/bin/env python

import rospy, sys, time
from moveit_commander import RobotCommander, MoveGroupCommander, roscpp_initialize, roscpp_shutdown
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Joy
from tf.transformations import quaternion_from_euler

class TeleopEffJoy():
    def __init__(self):
        roscpp_initialize(sys.argv)
        rospy.init_node('teleop_eff_joy')
        rospy.Subscriber('joy', Joy, self.callback)
        self.robot = RobotCommander()
        self.initRobot()
        self.button_list = dict()
        self.initButtons()





        p = PoseStamped()
        p.header.frame_id = 'up1_footprint'
        p.pose.position.x = 0.12792118579
        p.pose.position.y = -0.285290879999
        p.pose.position.z = 0.120301181892
        roll = 0
        pitch = 0
        yaw = -1.57 #pi/2 radians
        
        q = quaternion_from_euler(roll, pitch, yaw)
        p.pose.orientation.x = q[0]
        p.pose.orientation.y = q[1]
        p.pose.orientation.z = q[2]
        p.pose.orientation.w = q[3]

        self.button_list['a'].setPose(p)
        self.button_list['a'].setArm(MoveGroupCommander('right_arm'))





        rospy.spin()
        roscpp_shutdown()

    def initButtons(self):
        buttons = [['a',0],['b',1],['y',3],['LB',4],['back',8],['start',9],['power',16],['left_stick',10],['right_stick',11]]
        for button in buttons:
            self.button_list[button[0]] = Button(button[0],button[1])
    
    def initRobot(self):
        self.robot.right_arm.allow_replanning(True)
        self.robot.right_arm.allow_looking(True)
        self.robot.right_arm.set_goal_tolerance(0.05)
        self.robot.right_arm.set_planning_time(60)
        self.robot.right_arm.allow_replanning(True)
        self.robot.right_arm.allow_looking(True)
        self.robot.right_arm.set_goal_tolerance(0.05)
        self.robot.right_arm.set_planning_time(60)

    def callback(self, data):
        now = rospy.Time.now()
        
        for key, button in self.button_list.iteritems():
            if now > button.t_next:
                if data.buttons[button.button_id]:
                    button.doPose()
                    button.t_next = now + button.t_delta

class Button:
    def __init__(self, button_name, button_id):
        self.button_name = button_name
        self.button_id = button_id
        self.pose = 'none'
        self.arm = 'none'
        self.t_delta = rospy.Duration(.25)
        self.t_next = rospy.Time.now() + self.t_delta
        
    def setPose(self, pose):
        self.pose = pose
        
    def setArm(self, arm):
        self.arm = arm
        
    def doPose(self):
        if self.arm == 'none':
            rospy.loginfo('Arm not set for this button')
            return
        elif self.pose == 'none':
            rospy.loginfo('Pose not set for this button')
            return
        
        print 'Pose set: '
        print self.pose
        success = 0
        attempt = 0
        while not success:
            p_plan = self.arm.plan()
            attempt = attempt + 1
            rospy.loginfo('Planning attempt: ' + str(attempt))
            if p_plan.joint_trajectory.points != []:
                success = 1
        rospy.loginfo('Executing trajectory')
        self.arm.execute(p_plan)

if __name__ == '__main__':
    teleopArmJoy = TeleopEffJoy()

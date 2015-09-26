#!/usr/bin/env python

import rospy
import up1_manipulation.cartesian as up1_cartesian
import up1_manipulation.cartesian_approx as up1_cartesian_approx
import up1_robot.up1_robot as up1_robot
import up1_misc.boilerplate as up1_boilerplate

RESOLUTION = 0.05

if __name__ == "__main__":
    up1_boilerplate.setup('cartesian_demo')

    robot = up1_robot.Robot()
    arm = robot.right_arm.move_group
    gripper = robot.right_arm.gripper.move_group

    rospy.sleep(2)

    robot.right_arm.set_pose('rest')

    robot.right_arm.gripper.open()

    offset = [0, 0, 0.02]

    up1_cartesian.cartesian(arm, offset)

    up1_cartesian_approx.cartesian_approx(arm, offset, RESOLUTION)

    up1_boilerplate.teardown()

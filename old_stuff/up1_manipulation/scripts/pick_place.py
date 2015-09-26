#!/usr/bin/env python

import rospy
import up1_robot.up1_robot as up1_robot
import up1_manipulation.pick as up1_pick
import up1_misc.target_cube as up1_target
import up1_misc.calibration_rig as up1_rig
import up1_misc.scene_tools as up1_scene
import up1_misc.boilerplate as up1_boilerplate

# Note: the combination of right arm, picking from rig.right_pos,
# and placing at rig.middle_pos is the combination that has the
# most success.

if __name__ == "__main__":
    up1_boilerplate.setup('pick_demo')

    scene = up1_scene.Scene()
    scene.clear_all()

    rospy.sleep(2)

    rig = up1_rig.CalibrationRig()
    scene.set_color_by_name(rig, 'yellow')

    target = up1_target.Target(rig.right_pos)
    scene.set_color_by_name(target, 'blue')

    scene.send_colors()

    scene.add_target(target)
    scene.add_rig(rig)

    rospy.sleep(3)

    robot = up1_robot.Robot()

    robot.right_arm.set_pose('attack')

    rospy.sleep(2)

    robot.right_arm.gripper.open()

    rospy.sleep(1)

    up1_pick.pick(scene, robot.right_arm, target)
    up1_pick.place(scene, robot.right_arm, target, rig.middle_pos)

    robot.right_arm.set_pose('rest')

    rospy.sleep(2)

    up1_boilerplate.teardown()

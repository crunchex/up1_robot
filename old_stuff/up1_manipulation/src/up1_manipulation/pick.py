import rospy
import numpy as np
import copy


# Pick up the target using its initial pose
def pick(scene, arm, target):
    arm_group = arm.move_group

    # Pre-grasp approach position
    # TODO: figure out if this is really necessary or not
    arm_group.set_start_state_to_current_state()
    approach_position = copy.deepcopy(target.initial_position)
    approach_position[2] = approach_position[2] + 0.05
    arm_group.set_position_target(approach_position)
    traj = arm_group.go()

    rospy.sleep(4)

    # Get a trajectory plan
    arm_group.set_start_state_to_current_state()
    arm_group.set_position_target(target.initial_position)
    traj = arm_group.plan()

    rospy.sleep(2)

    # Execute the planned trajectory
    arm_group.execute(traj)

    rospy.sleep(2)

    gripper = arm.gripper.move_group
    gripper_pos = grasp(gripper)
    loosen_grip(gripper, gripper_pos)

    # Attach the target
    scene.interface.attach_box(arm_group.get_end_effector_link(), target.id, target.get_initial_pose(), target.size)


def place(scene, arm, target, xyz):
    arm_group = arm.move_group

    # Pre-drop approach position
    # TODO: figure out if this is really necessary or not
    arm_group.set_start_state_to_current_state()
    drop_position = copy.deepcopy(xyz)
    drop_position[2] = drop_position[2] + 0.05
    arm_group.set_position_target(drop_position)
    traj = arm_group.go()

    rospy.sleep(4)

    # Get a trajectory plan to a cm above the final target position
    # The arm just drops the object
    arm_group.set_start_state_to_current_state()
    target_position = copy.deepcopy(xyz)
    target_position[2] = target_position[2] + 0.01
    arm_group.set_position_target(xyz)
    traj = arm_group.plan()

    rospy.sleep(2)

    # Execute the planned trajectory
    arm_group.execute(traj)

    rospy.sleep(2)

    # Attach the target
    scene.interface.remove_attached_object(arm_group.get_end_effector_link(), target.id)


# Close the gripper around the target
# TODO: very dumb grasp planner - needs revising
def grasp(gripper_group):
    gripper_group.set_start_state_to_current_state()
    # Try increasingly larger grasps until a plan is successful
    for finger_pos in np.arange(0.0180, 0.0, -0.002):
        gripper_group.set_joint_value_target([finger_pos, finger_pos])
        traj = gripper_group.plan()

        if len(traj.joint_trajectory.points) != 0:
            gripper_group.execute(traj)
            rospy.sleep(2)
            return finger_pos

    return None


# Loosen the grip to undo collisions that may have occurred during grasp()
# Allows the arm to continue executing motion plans
def loosen_grip(gripper_group, gripper_pos):
    if gripper_pos is None:
        return

    gripper_group.set_joint_value_target([gripper_pos - 0.003, gripper_pos - 0.003])
    gripper_group.go()

    # Wait to execute
    rospy.sleep(2)
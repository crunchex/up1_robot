import numpy as np
from moveit_commander import MoveGroupCommander


class Robot:
    def __init__(self):
        self.left_arm = Arm('left')
        self.right_arm = Arm('right')


class Arm:
    def __init__(self, side):
        self.side = side

        # Set up the move group for the arm
        self.move_group = MoveGroupCommander(side + '_arm_group')
        self.tune()

        # Set up the gripper object
        self.gripper = Gripper(side)

    # Hardcoded tuning for the arm that can be tweaked later
    def tune(self):
        # Tolerance for position (meters) and orientation (radians)
        self.move_group.set_goal_position_tolerance(0.001)
        self.move_group.set_goal_orientation_tolerance(np.pi * 2)

        # Planning time in seconds
        self.move_group.allow_replanning(True)
        self.move_group.set_planning_time(10)

    def set_pose(self, pose_name):
        self.move_group.set_named_target(pose_name + '_' + self.side)
        self.move_group.go()


class Gripper:
    def __init__(self, side):
        self.side = side

        # Set up the move group for the gripper
        self.move_group = MoveGroupCommander(side + '_gripper_group')

    def open(self):
        self.move_group.set_named_target('open_' + self.side)
        self.move_group.go()
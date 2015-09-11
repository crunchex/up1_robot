import os
from geometry_msgs.msg import PoseStamped


class CalibrationRig:
    REFERENCE_FRAME = 'up1_footprint'

    id = 'rig'
    scale_tuple = (0.001, 0.001, 0.001)

    right_pos = [0.22, -0.093, 0.044]
    left_pos = [0.195, 0.1075, 0.044]
    far_pos = [0.303, 0.0475, 0.044]
    middle_pos = [0.17, 0.0, 0.012]

    def __init__(self):
        return

    def get_initial_pose(self):
        rig_pose = PoseStamped()
        rig_pose.header.frame_id = self.REFERENCE_FRAME
        rig_pose.pose.position.x = 0.0
        rig_pose.pose.position.y = 0.0
        rig_pose.pose.position.z = 0.05
        rig_pose.pose.orientation.w = 1.0
        return rig_pose

    @staticmethod
    def get_stl_path():
        relative_path = '/../../meshes/calibration_rig.stl'
        current_path = os.path.dirname(os.path.realpath(__file__))
        return current_path + relative_path

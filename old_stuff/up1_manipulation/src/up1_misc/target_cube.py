from geometry_msgs.msg import PoseStamped


class Target:
    REFERENCE_FRAME = 'up1_footprint'

    id = 'target'

    # Set the target size [l, w, h]
    size = [0.01, 0.01, 0.01]

    def __init__(self, initial_position):
        self.initial_position = initial_position

    def get_initial_pose(self):
        target_pose = PoseStamped()
        target_pose.header.frame_id = self.REFERENCE_FRAME
        target_pose.pose.position.x = self.initial_position[0]
        target_pose.pose.position.y = self.initial_position[1]
        target_pose.pose.position.z = self.initial_position[2]
        target_pose.pose.orientation.w = 1.0
        return target_pose
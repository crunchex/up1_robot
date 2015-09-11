import copy
from geometry_msgs.msg import Pose


def cartesian(arm, offset):
    waypoints = []
    
    # start with the current pose
    waypoints.append(arm.get_current_pose().pose)
    
    wpose = Pose()
    wpose.orientation.w = 1.0
    wpose.position.x = waypoints[0].position.x + offset[0]
    wpose.position.y = waypoints[0].position.y + offset[1]
    wpose.position.z = waypoints[0].position.z + offset[2]
    
    waypoints.append(copy.deepcopy(wpose))
    
    # We want the cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in cartesian translation.
    (cartesian_plan, fraction) = arm.compute_cartesian_path(
                                 waypoints,   # waypoints to follow
                                 0.005,       # eef_step
                                 0.01,        # jump_threshold
                                 True)        # allow collisions
    
    arm.execute(cartesian_plan)
    
    return fraction

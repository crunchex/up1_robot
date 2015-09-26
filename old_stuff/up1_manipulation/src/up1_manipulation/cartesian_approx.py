import copy
from geometry_msgs.msg import Pose
from math import floor


def cartesian_approx(arm, offset, resolution):
    current_pose = arm.get_current_pose()
    
    diff_x = float(offset[0])
    diff_y = float(offset[1])
    diff_z = float(offset[2])
    
    temp = abs(diff_x) if abs(diff_x) > abs(diff_y) else abs(diff_y)
    diff = temp if temp > abs(diff_z) else abs(diff_z)
    num_waypoints = int(floor(diff/resolution))
    
    if num_waypoints == 0:
        num_waypoints = 1
    
    step_x = diff_x/num_waypoints
    step_y = diff_y/num_waypoints
    step_z = diff_z/num_waypoints
    
    waypoints = []

    for idx in range(0, num_waypoints):
        current_pose.pose.position.x += step_x
        current_pose.pose.position.y += step_y
        current_pose.pose.position.z += step_z
        
        waypoints.append(copy.deepcopy(current_pose))
    
    for waypoint in waypoints:
        arm.set_pose_target(waypoint)
        traj = arm.plan()
        if traj.joint_trajectory.points != []:
            arm.execute(traj)
        else:
            print "Unable to plan waypoint"

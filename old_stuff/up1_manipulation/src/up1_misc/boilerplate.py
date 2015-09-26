import sys
import rospy
import moveit_commander


def setup(node_name):
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node(node_name)


def teardown():
    moveit_commander.roscpp_shutdown()
    moveit_commander.os._exit(0)
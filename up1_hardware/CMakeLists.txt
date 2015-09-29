cmake_minimum_required(VERSION 2.8.3)
project(up1_hardware)

find_package(catkin REQUIRED COMPONENTS roslaunch)

catkin_package()

# http://wiki.ros.org/roslaunch#Catkin
roslaunch_add_file_check(launch)

# TODO: create scripts for generating the ikfast cpp stuff.
install(DIRECTORY config launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

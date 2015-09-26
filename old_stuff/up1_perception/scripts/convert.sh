#!/usr/bin/env bash

rosrun camera_calibration_parsers convert /home/crunchex/uproot/catkin_ws/src/updroid_api/up1_perception/config/stereo_right.ini /home/crunchex/uproot/catkin_ws/src/updroid_api/up1_perception/config/stereo_right.yaml;
rosrun camera_calibration_parsers convert /home/crunchex/uproot/catkin_ws/src/updroid_api/up1_perception/config/stereo_left.ini /home/crunchex/uproot/catkin_ws/src/updroid_api/up1_perception/config/stereo_left.yaml;

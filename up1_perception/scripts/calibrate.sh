#!/usr/bin/env bash

rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.025 right:=/stereo/right/image_raw left:=/stereo/left/image_raw left_camera:=/stereo/left right_camera:=/stereo/right --approximate=0.05

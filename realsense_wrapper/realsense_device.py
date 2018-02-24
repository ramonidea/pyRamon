#!/usr/bin/env python3.5

# Depedency:
# Need to follow the instruction here to set up the machine and install python wrapper
# https://github.com/IntelRealSense/librealsense
#
#
# git clone https://github.com/IntelRealSense/librealsense
# cd librealsense
# mkdir build
# cd build
# cmake ../ -DBUILD_PYTHON_BINDINGS=TRUE
# make -j4
# sudo make install #Optional if you want the library to be installed in your system
#
#

import pyrealsense2 as rs
import numpy as np
import cv2

class visionsensor:
    def __init__(self, x = 640, y = 360, fps = 30):
        self.x = x
        self.y = y
        self.fps = fps

        self.depth = None
        self.rgb = None
        self.profile = None
        self.align = None
        self.align_to = None

        # Create a pipeline
        self.pipeline = rs.pipeline()
        #create a config
        self.config = rs.config()


    def load_settings(self):
        #low priority in implementing
        pass


    def get_camera_info(self):
        intrinsics = self.pipeline.get_active_profile().get_streams()[0].as_video_stream_profile().get_intrinsics()
        extrinsics = self.pipeline.get_active_profile().get_streams()[0].get_extrinsics_to(self.pipeline.get_active_profile().get_streams()[1])

        return str(intrinsics), str(extrinsics)
# TODO: Some processing data here to make to easy-to-be-separaable


    #Start the Color Camera
    def startCamera(self):
        # Start streaming
        self.profile = self.pipeline.start(self.config)
        #self.depth = profile.get_device().first_depth_sensor()

    #Stop the Depth Camera
    def stop(self):
        self.pipeline.stop()



    #Initialize color and depth camera (default 640 * 360 * 30fps)
    def createStreams(self):
        self.config.enable_stream(rs.stream.color, self.x, self.y, rs.format.bgr8, self.fps)
        self.config.enable_stream(rs.stream.depth, self.x, self.y, rs.format.z16, self.fps)



    #Enable the depth and color sync (un after initalized both cameras, before running them)
    def sync(self):
        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)


    #Return two frames from rgb and depth (aligned)
    def getFrame(self):
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()

        #Align the depth frame to color frames
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        #Return 3d Array
        color_image = np.asarray(color_frame.get_data())

        #Return 1D Array
        depth_image = np.asarray(aligned_depth_frame.get_data())
        depth_image = np.uint8(depth_image.astype(float) * 255 / 2 ** 12 - 1)
        #depth_image = 255 - cv2.cvtColor(depth_image, cv2.COLOR_GRAY2RGB)

        return color_image, depth_image
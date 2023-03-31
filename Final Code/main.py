#!/usr/bin/env python3
from movement import Drone, asyncio
from vision import Vision
from camera_config import CameraConfig
import cv2

''' This will me the main file ran combining both our movement and vision code '''

async def run():
	drone = Drone("")
	vision = Vision(cv2.VideoCapture(0))
	camera_config = CameraConfig()

	coordinate_thresh = 50 # How many pixels we allow before we tell the drone to move
	area_thresh = 200 # How much change in rectangle area we allow before we move forward/backward

	if(await drone.connect() == False):
		return

	await drone.takeoff()

	while(await drone.get_offboard_state() == True and vision.cap.isOpened()):
		vision.detect_color()

		if(vision.object_is_detected() and camera_config.check_config_status() == False):
			camera_config.set_config(vision.get_frame_area(), coordinate_thresh, area_thresh)

		elif(vision.object_is_detected() and camera_config.check_config_status() == True):
			# Handle x-axis/y-axis movements

			coordinates = vision.get_object_coordinates()

			if(coordinates[0] > -camera_config.coordinate_thresh):
				await drone.right(5.0, 4)

			elif(coordinates[0] < camera_config.coordinate_thresh):
				await drone.left(5.0, 4)

			elif(coordinates[1] > camera_config.coordinate_thresh):
				await drone.up(5.0, 4)

			elif(coordinates[1] < -camera_config.coordinate_thresh):
				await drone.down(5.0, 4)

			# Handle z-axis movements

			frame_area = vision.get_frame_area()

			if(frame_area > camera_config.initial_frame_area + camera_config.area_thresh):
				await drone.backward(5.0, 4)

			elif(frame_area < camera_config.initial_frame_area - camera_config.area_thresh):
				await drone.forward(5.0, 4)

	await vision.stop_all_detection()

	await drone.land()

	await drone.disconnect()


if __name__ == '__main__':
	asyncio.run(run())

#!/usr/bin/env python3
from movement import Drone, asyncio
from vision import Vision
import cv2

''' This will me the main file ran combining both our movement and vision code '''

async def run():
	drone = Drone("")
	vision = Vision(cv2.VideoCapture(0))

	if(await drone.connect() == False):
		return

	await drone.takeoff()

	while(await drone.get_offboard_state() == True and vision.cap.isOpened()):
		vision.detect_color()

		if(vision.object_is_detected()):
			# Handle x-axis/y-axis movements

			coordinates = vision.get_object_coordinates()

			if(coordinates[0] > 0):
				await drone.right(5.0, 4)

			elif(coordinates[0] < 0):
				await drone.left(5.0, 4)

			elif(coordinates[1] > 0):
				await drone.up(5.0, 4)

			elif(coordinates[1] < 0):
				await drone.down(5.0, 4)

			# Handle z-axis movements

			frame_area = vision.get_frame_area()

			if(frame_area > 100):
				await drone.backward(5.0, 4)

			elif(frame_area < 100):
				await drone.forward(5.0, 4)

	await vision.stop_all_detection()

	await drone.land()

	await drone.disconnect()


if __name__ == '__main__':
	asyncio.run(run())

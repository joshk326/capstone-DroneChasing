#!/usr/bin/env python3
from movement import Drone, asyncio
from vision import Vision
from object_config import ObjectConfig
import cv2

''' This will me the main file ran combining both our movement and vision code '''

async def run():
	drone = Drone("")
	vision = Vision(cv2.VideoCapture(0))
	detectedObj = ObjectConfig()

	coordinate_thresh = 50 # How many pixels we allow before we tell the drone to move
	area_thresh = 200 # How much change in rectangle area we allow before we move forward/backward

	if(await drone.connect() == False):
		return

	await drone.takeoff()

	while(await drone.get_offboard_state() == True and vision.cap.isOpened()):
		vision.detect_color()
		area = vision.get_box_area()
		box_dim = vision.get_box_dimenstions()
		if(vision.object_is_detected() and detectedObj.check_detected_status() == False):
			#detectedObj.set_config(vision.get_box_area(), coordinate_thresh, area_thresh)
			detectedObj.update_detected_status(True)
			detectedObj.set_config(area, box_dim, coordinate_thresh, area_thresh)
			print("-- Object Detected")
		elif(vision.object_is_detected() and detectedObj.check_detected_status() == True):
			# Handle x-axis/y-axis movements
			print(detectedObj.get_intial_area())
			
			coordinates = vision.get_object_coordinates()

			# if(coordinates[0] > -detectedObj.coordinate_thresh):
			# 	await drone.right(5.0, 4.0)

			# elif(coordinates[0] < detectedObj.coordinate_thresh):
			# 	await drone.left(5.0, 4.0)

			# elif(coordinates[1] > detectedObj.coordinate_thresh):
			# 	await drone.up(5.0, 4.0)

			# elif(coordinates[1] < -detectedObj.coordinate_thresh):
			# 	await drone.down(5.0, 4.0)

			# Handle z-axis movements

			frame_area = vision.get_box_area()

			# if(get_box_area > detectedObj.initial_frame_area + detectedObj.area_thresh):
			# 	await drone.backward(5.0, 4.0)

			# elif(get_box_area < detectedObj.initial_frame_area - detectedObj.area_thresh):
			# 	await drone.forward(5.0, 4.0)

			if cv2.waitKey(25) & 0xFF == ord('q'):
				break

		

	vision.stop_all_detection()

	await drone.land()

	await drone.disconnect()


if __name__ == '__main__':
	asyncio.run(run())

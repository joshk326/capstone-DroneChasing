#!/usr/bin/env python3
from movement import Drone, asyncio
from vision import Vision
from object_config import ObjectConfig
from threading import Thread
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

	await drone.takeoff(altitude=1.0)
	
	vision_thread = Thread(target=vision.detect_color)
	vision_thread.start()

	while(await drone.get_offboard_state() == True and vision.is_detecting):
		area = vision.get_box_area()
		box_dim = vision.get_box_dimenstions()
		if(vision.object_is_detected() and detectedObj.check_detected_status() == False):
			detectedObj.update_detected_status(True)
			detectedObj.set_config(area, box_dim, coordinate_thresh, area_thresh)
			print("\n-- Object Detected\n")
		elif(vision.object_is_detected() and detectedObj.check_detected_status() == True):
			#print(detectedObj.get_intial_area())
			
			coordinates = vision.get_object_coordinates()
			#print(coordinates)

			diff = vision.get_center_diff()
			move_x = vision.convert_px_to_m(abs(diff[0]))
			move_y = vision.convert_px_to_m(abs(diff[1]))

			if coordinates[0] < detectedObj.coordinate_thresh:
				await drone.left(move_x, 1.0)
			elif coordinates[0] > -detectedObj.coordinate_thresh:
				await drone.right(move_x, 1.0)
			if coordinates[1] < -detectedObj.coordinate_thresh:
				await drone.down(move_y, 1.0)
			elif coordinates[1] > detectedObj.coordinate_thresh:
				await drone.up(move_y, 1.0)

			frame_area = vision.get_box_area()

			if(frame_area > detectedObj.initial_frame_area + detectedObj.area_thresh):
				await drone.backward(5.0, 4.0)
			elif(frame_area < detectedObj.initial_frame_area - detectedObj.area_thresh):
				await drone.forward(5.0, 4.0)

		
	vision_thread.join()
	vision.stop_all_detection()

	await drone.land()

	await drone.disconnect()


if __name__ == '__main__':
	asyncio.run(run())

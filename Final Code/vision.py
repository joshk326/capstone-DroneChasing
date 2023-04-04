#!/usr/bin/env python3
import cv2
import numpy as np
import imutils

class Vision():

	_lower_red = np.array([0, 120, 70])
	_upper_red = np.array([10, 255, 255])
	_lower_red2 = np.array([170, 120, 70])
	_upper_red2 = np.array([180, 255, 255])

	_frame_width = 500
	_frame_height = 500

	_x, _y, _w, _h = 0, 0, 0, 0

	object_detected = False

	def __init__(self, camera):
		self.cap = camera

		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._frame_width)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._frame_height)

		self.hog = cv2.HOGDescriptor()
		self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

		self.x_diff = 0
		self.y_diff = 0

	def _center_diff(self, frame_center, detected_center):
		x_diff = frame_center[0] - detected_center[0]
		y_diff = frame_center[1] - detected_center[1]
		return (x_diff, y_diff)
	
	def get_object_coordinates(self):
		return (self.x_diff, self.y_diff)
	
	def get_box_dimenstions(self):
		return [self._w, self._h]
	
	def get_box_area(self):
		return self._w * self._h

	def object_is_detected(self):
		return self.object_detected
	
	def detect_color(self):
		ret, frame = self.cap.read()

		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, 'FPS: ' + str(self.cap.get(cv2.CAP_PROP_FPS)), (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

		frame_center = (int(640/2), int(self._frame_height/2))
		cv2.circle(frame, frame_center, 5, (255, 0, 0), -1)

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask1 = cv2.inRange(hsv, self._lower_red, self._upper_red)
		mask2 = cv2.inRange(hsv, self._lower_red2, self._upper_red2)
		mask = mask1 + mask2
		cv2.imshow("Frame",mask)
		contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		if len(contours) > 0:
			if not self.object_detected:
				largest_contour = max(contours, key=cv2.contourArea)
				self._x, self._y, self._w, self._h = cv2.boundingRect(largest_contour)
				self.object_detected = True
			else:
				largest_contour = max(contours, key=cv2.contourArea)
				self._x, self._y, self._w, self._h = cv2.boundingRect(largest_contour)

		
		cv2.rectangle(frame, (self._x, self._y), (self._x+self._w, self._y+self._h), (0, 255, 0), 2)
		cv2.putText(frame, "Tracked Object Cords: X- " + str(self._x) + " Y- " + str(self._y), (self._frame_width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		detected_center = (int(self._x+self._w/2), int(self._y+self._h/2))
		cv2.circle(frame, detected_center, 5, (255, 0, 0), -1)

		x_diff, y_diff = self._center_diff(frame_center, detected_center)
		cv2.putText(frame, "X Diff: " + str(x_diff) + " Y Diff: " + str(y_diff), (self._frame_width-200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		cv2.putText(frame, "Frame Height: " + str(self._h) + " Frame Width: " + str(self._w), (self._frame_width-200, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		cv2.imshow('Tracked Object', frame)

	def stop_all_detection(self):
		self.cap.release()
		cv2.destroyAllWindows()


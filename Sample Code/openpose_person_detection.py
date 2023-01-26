import cv2
import openpose as op

# Create a capture object for the video stream
cap = cv2.VideoCapture(0)

# Create an OpenPose object
openpose = op.OpenPose()

# Define the termination criteria for the CAMShift algorithm
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

prev_people = 0

while True:
# Read the next frame from the video stream
	ret, frame = cap.read()

	# Detect the human body parts in the frame
	body_parts, _ = openpose.forward(frame, True)
	people = len(body_parts)

	if people == 1:
	# Extract the coordinates of the upper body joints
		upper_body_joints = body_parts[2]

		# Define the initial bounding box for the upper body
		x, y, w, h = cv2.boundingRect(upper_body_joints)
		bbox = (x, y, w, h)

		# Convert the frame to the HSV color space
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Create a mask for the upper body color
		mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 30))

		# Perform the CAMShift algorithm
		retval, bbox = cv2.CamShift(mask, bbox, termination)

		# Draw the bounding box on the frame
		cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (255, 0, 0), 2)

		# Show the frame
		cv2.imshow("Tracked Object", frame)

	# Break the loop if the 'q' key is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release the capture object
cap.release()

# Close all the windows
cv2.destroyAllWindows()

import cv2
import numpy as np


lower_red = np.array([0,100,100])
upper_red = np.array([20,255,255])
# lower_red = np.array([30, 150, 50])
# upper_red = np.array([255, 255, 180])
# lower_red2 = np.array([170, 50, 50])
# upper_red2 = np.array([180, 255, 255])

# Open the computer's camera
cap = cv2.VideoCapture(0)

# Initialize the coordinates of the tracked face
x, y, w, h = 0, 0, 0, 0


object_detected = False


# Continuously read frames from the camera and track the first detected face
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'FPS: ' + str(cap.get(cv2.CAP_PROP_FPS)), (10, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Capture - Face detection', frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    #mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    #mask = mask1 + mask2
    cv2.imshow("Frame",mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    # Check if at least one face is detected
    if len(contours) > 0:
        if not object_detected:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            object_detected = True
        # If the object has been detected before, track the largest detected object
        else:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
        # # Track the first detected face
        # x, y, w, h = faces[0]

    # Print the coordinates of the tracked face
    print(f"Coordinates of the tracked red object: x={x}, y={y}, width={w}, height={h}")

    # Draw a rectangle around the tracked face (for visualization purposes only)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the output frame with the tracked face
    cv2.imshow('Tracked Object', frame)

    # Wait for a key press and check if it's the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()


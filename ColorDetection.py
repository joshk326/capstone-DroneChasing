import cv2
import numpy as np


lower_red = np.array([30, 150, 50])
upper_red = np.array([255, 255, 180])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

frame_width = 500
frame_height = 500


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

x, y, w, h = 0, 0, 0, 0


object_detected = False

def center_diff(frame_center, detected_center):
    x_diff = frame_center[0] - detected_center[0]
    y_diff = frame_center[1] - detected_center[1]
    return (x_diff, y_diff)

while cap.isOpened():
    ret, frame = cap.read()

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'FPS: ' + str(cap.get(cv2.CAP_PROP_FPS)), (10, 50), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    frame_center = (int(640/2), int(frame_height/2))
    cv2.circle(frame, frame_center, 5, (255, 0, 0), -1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2
    cv2.imshow("Frame",mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    

    if len(contours) > 0:
        if not object_detected:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            object_detected = True
        else:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

    
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, "Tracked Object Cords: X- " + str(x) + " Y- " + str(y), (frame_width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    detected_center = (int(x+w/2), int(y+h/2))
    cv2.circle(frame, detected_center, 5, (255, 0, 0), -1)

    x_diff, y_diff = center_diff(frame_center, detected_center)
    cv2.putText(frame, "X Diff: " + str(x_diff) + " Y Diff: " + str(y_diff), (frame_width-200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Tracked Object', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

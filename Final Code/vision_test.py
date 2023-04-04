from vision import Vision
import cv2

vision = Vision(cv2.VideoCapture(0))

while(1):
    vision.detect_color()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
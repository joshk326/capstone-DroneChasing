import cv2 as cv

def detectAndDisplay(frame):
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	frame_gray = cv.equalizeHist(frame_gray)
	#-- Detect faces
	faces = face_cascade.detectMultiScale(frame_gray)
	for (x,y,w,h) in faces:
		center = (x + w//2, y + h//2)
		frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 0, 255), 4)
		print('Face found at', center)

	font = cv.FONT_HERSHEY_SIMPLEX
	cv.putText(frame, 'FPS: ' + str(cap.get(cv.CAP_PROP_FPS)), (10, 50), font, 1, (0, 0, 255), 2, cv.LINE_AA)
	cv.imshow('Capture - Face detection', frame)


face_cascade_name = "data/face.xml"
face_cascade = cv.CascadeClassifier()

if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

camera_device = 1

cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)


while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:#esc key
        break

cap.release()
cv.destroyAllWindows()
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    succes, frame = cap.read()
    if succes:
        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1)== ord('q'):
            break

cv2.destroyAllWindows()
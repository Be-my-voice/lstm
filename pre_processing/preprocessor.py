import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture("break_1.avi")

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgbFrame)

    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    print(results.pose_landmarks)

    cv2.imshow('skeleton', frame)

    cv2.waitKey(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    break
    
cap.release()
cv2.destroyAllWindows()
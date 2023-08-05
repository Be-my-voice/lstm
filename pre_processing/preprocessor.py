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
    
    # print(results.pose_landmarks)
    with open("break_1.csv", mode='a', newline='') as file:
        j = results.pose_landmarks.landmark[0]
        res = str(j.x) +','+ str(j.y)
        file.write(res)
        for i in range(1,33):
            j = results.pose_landmarks.landmark[i]
            print(j.x , j.y)
            res = ',' + str(j.x) +','+ str(j.y)
            file.write(res)
        file.write("\n")

    cv2.imshow('skeleton', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
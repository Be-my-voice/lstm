import mediapipe as mp
import cv2
from mediapipe.framework.formats import landmark_pb2
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def this(filename):
    cap = cv2.VideoCapture("src_original/"+filename)
    fnameWithoutExtension = os.path.splitext(filename)[0]
    start = 1
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgbFrame)

        finalRes = landmark_pb2.NormalizedLandmarkList(landmark = results.pose_landmarks.landmark[11:23])

        # connections = frozenset({(4, 10), (5, 9), (7, 9), (3, 5),  (4, 6), (5, 11), (0, 2), (4, 8), (5, 7), (1, 3), (6, 8),  (2, 4)})

        # if results.pose_landmarks:
        #     mp.solutions.drawing_utils.draw_landmarks(frame, finalRes, connections)
        
        # for i in finalRes.landmark:
        #     print(i.x, i.y)
        with open("outs/"+fnameWithoutExtension+".csv", mode='a', newline='') as file:
            if start==0:
                file.write("\n")

            j = finalRes.landmark[0]
            res = str(j.x) +','+ str(j.y)
            # print(j.x , j.y)
            file.write(res)

            for i in range(1,12):
                j = finalRes.landmark[i]
                # print(j.x , j.y)
                res = ',' + str(j.x) +','+ str(j.y)
                file.write(res)
            
            start = 0
            

    #     cv2.imshow('skeleton', frame)
        
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()

# this("break_2.avi")
files = os.listdir("src_original")
for name in files:
    print("processing : "+name)
    this(name)
    print("completed : "+name)
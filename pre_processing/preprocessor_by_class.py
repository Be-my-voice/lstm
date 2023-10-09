# extract skeleton data from original video files by class names
# input videos seperated into different directories by class name eg -  /src_origina/break
# csv file per video containing x,y value for skelton points

import os
import shutil
import mediapipe as mp
import cv2
from mediapipe.framework.formats import landmark_pb2
import os
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Copy folder structure of src_original into output folder
def copy_folder_structure(source_folder, target_folder):
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    
    # Create the target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Walk through the source folder's directory tree
    for root, _, files in os.walk(source_folder):
        # Calculate the relative path from the source to the current folder
        relative_path = os.path.relpath(root, source_folder)
        # Construct the corresponding path in the target folder
        target_path = os.path.join(target_folder, relative_path)
        
        # Create the corresponding folder in the target folder
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    print(f"Folder structure from '{source_folder}' copied to '{target_folder}'.")



# Convert a video file into landmakrs csv
def this(src_file):
    cap = cv2.VideoCapture(src_file)
    fnameWithoutExtension = os.path.splitext(src_file)[0]
    target_file = src_file.replace("/src_original/", "/preprocessed_data/").replace(".mp4", ".csv")

    print(src_file)

    start = 1
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgbFrame)

        finalRes = landmark_pb2.NormalizedLandmarkList(landmark = results.pose_landmarks.landmark[11:23])

        connections = frozenset({(4, 10), (5, 9), (7, 9), (3, 5),  (4, 6), (5, 11), (0, 2), (4, 8), (5, 7), (1, 3), (6, 8),  (2, 4)})

        # if results.pose_landmarks:
        #     mp.solutions.drawing_utils.draw_landmarks(frame, finalRes, connections)
        
        # for i in finalRes.landmark:
        #     print(i.x, i.y)
        with open(target_file, mode='a', newline='') as file:
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

        # Draw skeleton
        blank_frame = np.zeros_like(frame)
        line_drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=25, circle_radius=1)
        joint_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=25, circle_radius=2)
        mp_drawing.draw_landmarks(blank_frame, finalRes, connections, landmark_drawing_spec=line_drawing_spec, connection_drawing_spec=joint_drawing_spec)
        # cv2.imshow('skeleton', blank_frame)
        # End draw skeleton
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def preprocess_all_files(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            this(file_path)


source_folder = os.getcwd() + "/pre_processing/src_original/"
target_folder = os.getcwd() + "/pre_processing/preprocessed_data/"
# Copy folder structure
# copy_folder_structure(source_folder, target_folder)

# Example data preprocess for a single file
# this(os.getcwd() + "/pre_processing/src_original/break/break_1.mp4")

preprocess_all_files(os.getcwd() + "/pre_processing/src_original/")

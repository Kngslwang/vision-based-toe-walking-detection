import mediapipe as mp
import cv2
import os
import json
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def angle_calc(mat):
    x1 = mat[0, 0]
    y1 = mat[0, 1]
    x2 = mat[1, 0]
    y2 = mat[1, 1]
    x4 = mat[3, 0]
    y4 = mat[3, 1]
    angle = np.arccos(((x1 - x2) * (x2 - x4) + (y1 - y2) * (y2 - y4))
                              / np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / np.sqrt((x2 - x4) ** 2 + (y2 - y4) ** 2))
    return angle


def dis_calc(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


annotations = 'landing-foot-recognition/annotation'
images = 'landing-foot-recognition/images'
# cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
# cv2.resizeWindow("output", 400, 300)
estimated_data = np.zeros((4, 2))
output = {}
diff_angle_list = []
pck_list = []
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    for file in os.listdir(images):
        data = np.zeros((4, 2))
        img = os.path.join(images, file)
        annotation = os.path.join(annotations, file.replace('png', 'json'))
        with open(annotation, 'r+') as f:
            gt = json.load(f)
        for i in range(4):
            if gt['shapes'][i]['label'] == 'knee':
                data[0, :] = gt['shapes'][i]['points'][0]
            elif gt['shapes'][i]['label'] == 'ankle':
                data[1, :] = gt['shapes'][i]['points'][0]
            elif gt['shapes'][i]['label'] == 'heel':
                data[2, :] = gt['shapes'][i]['points'][0]
            elif gt['shapes'][i]['label'] == 'index':
                data[3, :] = gt['shapes'][i]['points'][0]

        image = cv2.imread(img)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks == None:
            output[file] = {'detected': 0}
            continue
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        '''
        for i in range(data.shape[0]):
            cv2.circle(image, (int(data[i][0]), int(data[i][1])), 5, (21,123,0), 10)
        cv2.imshow('output', image)
        '''
        cv2.imshow('output', image)
        pressedKey = cv2.waitKey(100000)
        if pressedKey == ord('l'):
            key = [25, 27, 29, 31]
            estimated_data[0, :] = [results.pose_landmarks.landmark[key[0]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[0]].y * image.shape[0]]
            estimated_data[1, :] = [results.pose_landmarks.landmark[key[1]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[1]].y * image.shape[0]]
            estimated_data[2, :] = [results.pose_landmarks.landmark[key[2]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[2]].y * image.shape[0]]
            estimated_data[3, :] = [results.pose_landmarks.landmark[key[3]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[3]].y * image.shape[0]]
            '''
            for i in range(data.shape[0]):
                cv2.circle(image, (int(estimated_data[i][0]), int(estimated_data[i][1])), 5, (121,123,0), 10)
            cv2.imshow('output', image)
            '''
            cv2.imshow('output', image)
            pressedKey2 = cv2.waitKey(100000)
            if pressedKey2 != pressedKey:
                key = [26, 28, 30, 32]
                estimated_data[0, :] = [results.pose_landmarks.landmark[key[0]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[0]].y * image.shape[0]]
                estimated_data[1, :] = [results.pose_landmarks.landmark[key[1]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[1]].y * image.shape[0]]
                estimated_data[2, :] = [results.pose_landmarks.landmark[key[2]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[2]].y * image.shape[0]]
                estimated_data[3, :] = [results.pose_landmarks.landmark[key[3]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[3]].y * image.shape[0]]

        elif pressedKey == ord('r'):
            key = [26, 28, 30, 32]
            estimated_data[0, :] = [results.pose_landmarks.landmark[key[0]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[0]].y * image.shape[0]]
            estimated_data[1, :] = [results.pose_landmarks.landmark[key[1]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[1]].y * image.shape[0]]
            estimated_data[2, :] = [results.pose_landmarks.landmark[key[2]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[2]].y * image.shape[0]]
            estimated_data[3, :] = [results.pose_landmarks.landmark[key[3]].x * image.shape[1],
                                    results.pose_landmarks.landmark[key[3]].y * image.shape[0]]
            '''
            for i in range(data.shape[0]):
                cv2.circle(image, (int(estimated_data[i][0]), int(estimated_data[i][1])), 5, (121,123,0), 10)
            cv2.imshow('output', image)
            '''
            cv2.imshow('output', image)
            pressedKey2 = cv2.waitKey(100000)
            if pressedKey2 != pressedKey:
                key = [25, 27, 29, 31]
                estimated_data[0, :] = [results.pose_landmarks.landmark[key[0]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[0]].y * image.shape[0]]
                estimated_data[1, :] = [results.pose_landmarks.landmark[key[1]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[1]].y * image.shape[0]]
                estimated_data[2, :] = [results.pose_landmarks.landmark[key[2]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[2]].y * image.shape[0]]
                estimated_data[3, :] = [results.pose_landmarks.landmark[key[3]].x * image.shape[1],
                                        results.pose_landmarks.landmark[key[3]].y * image.shape[0]]
        else:
            output[file] = {'detected': 0}
            continue
        # ankle difference calculation
        angle_predict = angle_calc(estimated_data)
        angle_truth = angle_calc(data)
        diff = abs(angle_truth - angle_predict) / angle_truth
        diff_angle_list.append(diff)

        # pck calculation
        thres = 0.2
        head1 = [results.pose_landmarks.landmark[7].x * image.shape[1],
                                        results.pose_landmarks.landmark[7].y * image.shape[0]]
        head2 = [results.pose_landmarks.landmark[8].x * image.shape[1],
                                        results.pose_landmarks.landmark[8].y * image.shape[0]]
        head_distance = dis_calc(head1, head2)
        count = 0
        for i in range(4):
            part_dis = dis_calc(estimated_data[i, :], data[i, :])
            if part_dis / head_distance <= thres:
                count += 1
        pck = count / 4.
        pck_list.append(pck)
        output[file] = {'knee': list(estimated_data[0, :]), 'ankle': list(estimated_data[1, :]),
                        'heel': list(estimated_data[2, :]), 'index': list(estimated_data[3, :]),
                        'angle_diff': diff, 'pck': pck, 'detected': 1}
print('pck:')
print(np.mean(pck_list))
print('angle_difference: ')
print(np.mean(diff_angle_list))
'''
with open('output.txt', 'w+') as f:
    json.dump(output, f)
'''



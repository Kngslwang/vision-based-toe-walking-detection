import os
import cv2
import shutil


samples = []
files = 'Zero-Occlusion-Object-Tracking-Data-Set-master'

for i in range(1, 21):
    if i < 10:
        samples.append('000' + str(i) + '.png')
    else:
        samples.append('00' + str(i) + '.png')
count = 0
for file in os.listdir(files):
    for sample in samples:
        img = cv2.imread(os.path.join(files, file, sample))
        cv2.imshow('1', img)
        pressedKey = cv2.waitKey(100000)
        if pressedKey == ord('s'):
            # landing foot
            count += 1
            saving_files = os.path.join(files, file, sample)
            shutil.copy(os.path.join(files, file, sample), 'new_dataset')
            os.rename(os.path.join('new_dataset', sample), os.path.join('new_dataset', str(count) + '.png'))
            continue

        elif pressedKey == ord('j'):
            continue

for i in saving_files:
    shutil.copy(i, 'new_dataset')

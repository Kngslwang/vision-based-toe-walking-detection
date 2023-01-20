import os
import cv2
import json

dataset = 'landing-foot-recognition/images'

distance = {'1': [], '2': [], '3': [], '4': []}
types = {'elevator shoes': [], 'ankle shoes': [], 'long boots': [], 'others': []}

cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
cv2.resizeWindow("output", 400, 300)

print('processing distance')
for file in os.listdir(dataset):

    img = os.path.join(dataset, file)
    image = cv2.imread(img)
    cv2.imshow("output", image)
    pressedKey = cv2.waitKey(100000)
    if pressedKey == ord('1'):
        distance['1'].append(img)

    elif pressedKey == ord('2'):
        distance['2'].append(img)
    elif pressedKey == ord('3'):
        distance['3'].append(img)
    elif pressedKey == ord('4'):
        distance['4'].append(img)


with open('distance.txt', 'w+') as f:
    json.dump(distance, f)


print('processing type shoe')
for file in os.listdir(dataset):

    img = os.path.join(dataset, file)
    image = cv2.imread(img)
    cv2.imshow("output", image)
    pressedKey = cv2.waitKey(100000)
    if pressedKey == ord('1'):
        types['elevator shoes'].append(img)

    elif pressedKey == ord('2'):
        types['ankle shoes'].append(img)
    elif pressedKey == ord('3'):
        types['long boots'].append(img)
    elif pressedKey == ord('4'):
        types['others'].append(img)

with open('types.txt', 'w+') as f:
    json.dump(types, f)

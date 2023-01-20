import os
import cv2
import json

with open('distance.txt', 'r+') as f:
    distance = json.load(f)

with open('types.txt', 'r+') as f:
    types = json.load(f)
a = 3
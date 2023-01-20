import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_sum = {}
file_numpy = np.zeros((123, 5))
with open('pck.txt', 'r+') as f1:
    pck = json.load(f1)

with open('distance.txt', 'r+') as f2:
    distances = json.load(f2)

with open('types.txt', 'r+') as f3:
    types = json.load(f3)

with open('output.txt', 'r+') as f4:
    outputs = json.load(f4)

num = -1
for file in outputs.keys():

    if outputs[file]['detected'] == 0:
        file_sum[file] = {'detected': 0}

        continue
    if file in ['115.png', '116.png', '117.png']:
        continue
    file_address = os.path.join('landing-foot-recognition/images', file)
    pck_one = pck[file]

    for dis in distances.keys():
        if file_address in distances[dis]:
            break

    for type_one in types.keys():
        if file_address in types[type_one]:
            break

    angle_diff = outputs[file]['angle_diff']

    file_sum[file] = {'pck': pck_one, 'distance': dis, 'type': type_one, 'angle difference': angle_diff, 'detected': 1}
    num += 1
    
    
    file_numpy[num, 0] = float(file.split('.')[0])
    file_numpy[num, 1] = pck_one
    file_numpy[num, 2] = float(dis)
    file_numpy[num, 3] = angle_diff

    if type_one == 'ankle shoes':
        file_numpy[num, 4] = 1
    elif type_one == 'long boots':
        file_numpy[num, 4] = 2
    else:
        file_numpy[num, 4] = 3


# with open('file_sum.txt', 'w+') as f:
#     json.dump(file_sum, f)
# np.savetxt('frame.csv', file_numpy, delimiter=',')


dis_box_angle = np.array([file_numpy[file_numpy[:, 2] == 1, 3], file_numpy[file_numpy[:, 2] == 2, 3],
                          file_numpy[file_numpy[:, 2] == 3, 3], file_numpy[file_numpy[:, 2] == 4, 3]])
dis_box_pck = np.array([file_numpy[file_numpy[:, 2] == 1, 1], file_numpy[file_numpy[:, 2] == 2, 1],
                        file_numpy[file_numpy[:, 2] == 3, 1], file_numpy[file_numpy[:, 2] == 4, 1]]) * 100.

type_box_angle = np.array([file_numpy[file_numpy[:, 4] == 1, 3], file_numpy[file_numpy[:, 4] == 2, 3],
                          file_numpy[file_numpy[:, 4] == 3, 3]])
type_box_pck = np.array([file_numpy[file_numpy[:, 4] == 1, 1], file_numpy[file_numpy[:, 4] == 2, 1],
                         file_numpy[file_numpy[:, 4] == 3, 1]]) * 100.

plt.figure(figsize=(12, 12))

plt.subplot(221)
plt.boxplot(dis_box_angle)
plt.xticks(range(1, 5), ['Very Close', 'Close', 'Far', 'Very Far'], size=16)
plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0%', '20%', '40%', '60%', '80%', '100%'], size=18)
plt.xlabel('Distance', size=18)
plt.ylabel('Angle Difference', size=18)

plt.subplot(222)
plt.boxplot(dis_box_pck)
plt.xticks(range(1, 5), ['Very Close', 'Close', 'Far', 'Very Far'], size=16)
plt.yticks(size=16)
plt.xlabel('Distance', size=18)
plt.ylabel('PCK@0.2', size=18)

plt.subplot(223)
plt.boxplot(type_box_angle)
plt.xticks(range(1, 4), ['Ankle Shoes', 'Long Boots', 'Others'], size=16)
plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0%', '20%', '40%', '60%', '80%', '100%'], size=18)
plt.xlabel('Types of Shoes', size=18)
plt.ylabel('Angle Difference', size=18)

plt.subplot(224)
plt.boxplot(type_box_pck)
plt.xticks(range(1, 4), ['Ankle Shoes', 'Long Boots', 'Others'], size=16)
plt.yticks(size=16)
plt.xlabel('Types of Shoes', size=18)
plt.ylabel('PCK@0.2', size=18)

plt.savefig('1.png', bbox_inches='tight', dpi=1200)

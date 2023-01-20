import os
import json
import numpy as np


def dis_calc(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


annotations = 'landing-foot-recognition/annotation'
head_lengths = 'landing-foot-recognition/headlength'
joints = ['knee', 'ankle', 'heel', 'index']
pck_list = []
pck_dict = {}


with open('output.txt', 'r+') as f:
    output = json.load(f)
    for file in output.keys():
        if output[file]['detected'] == 0:
            continue
        with open(os.path.join(annotations, file.replace('png', 'json')), 'r+') as f:
            annotation = json.load(f)

        with open(os.path.join(head_lengths, file.replace('png', 'json')), 'r+') as f:
            head_length_file = json.load(f)

        head_length = dis_calc(head_length_file['shapes'][0]['points'][0], head_length_file['shapes'][0]['points'][1])

        # calculation distances
        distances = []
        for joint in joints:
            for i in annotation['shapes']:
                if i['label'] == joint:
                    distances.append(dis_calc(output[file][joint], i['points'][0]))
                    continue

        # pck calculation
        thres = 0.2
        count = 0
        for i in range(4):
            part_dis = distances[i]
            if part_dis / head_length <= thres:
                count += 1
        pck = count / 4.
        pck_list.append(pck)
        pck_dict[file] = pck
with open('pck.txt', 'w+') as f:
    json.dump(pck_dict, f)
print(np.mean(pck_list))



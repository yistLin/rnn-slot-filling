#!/usr/local/bin/python3
import sys
import json
from os import listdir
from os.path import isdir, isfile, join

try:
    data_path = sys.argv[1]
except Except as e:
    print('Error:', str(e))
    sys.exit(-1)

cnt = 1

trans_list = []
cam_list = []

for f in listdir(data_path):
    out_dir = join(data_path, f)
    if not isdir(out_dir):
        continue

    print('Into Directory [%s]' % out_dir)
    for voip_dir in listdir(out_dir):
        in_dir = join(out_dir, voip_dir)
        if not isdir(in_dir):
            continue
        label_path = in_dir + '/label.json'
        # print('[%d] path=%s' % (cnt, label_path))
        # cnt += 1
        with open(label_path, 'r') as label_file:
            obj = json.loads(label_file.read())
            isSuccess = obj['task-information']['feedback']['success']
            if isSuccess:
                turns = obj['turns']
                for turn in turns:
                    trans = turn['transcription']
                    cam = turn['semantics']['cam']
                    # print('  trans: ' + trans)
                    # print('    cam: ' + cam)
                    # print()
                    trans_list.append(trans)
                    cam_str = []
                    for str_type in cam.split('|'):
                        if 'dontcare' in str_type:
                            cam_str.append('dontcare')
                            break
                        action = str_type[:str_type.find('(')]
                        content = str_type[str_type.find('(')+1:str_type.find(')')]
                        slot_content = []
                        if len(content) != 0:
                            for slot in content.split(','):
                                if '=' not in slot:
                                    slot_content.append(slot)

                        if len(slot_content) != 0:
                            cam_str.append(action + ' : ' + ' '.join(slot_content))
                        else:
                            cam_str.append(action)
                    cam_list.append(' | '.join(cam_str))

with open('X_train', 'w') as x_file:
    x_file.write('\n'.join(trans_list) + '\n')

with open('Y_train', 'w') as y_file:
    y_file.write('\n'.join(cam_list) + '\n')

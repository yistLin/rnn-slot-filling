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
slots_list = []

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
                    trans_list.append(trans)
                    for str_type in cam.split('|'):
                        if 'dontcare' in str_type:
                            continue

                        action = str_type[:str_type.find('(')]
                        content = str_type[str_type.find('(')+1:str_type.find(')')]

                        if len(content) == 0:
                            continue

                        slot_content = []
                        for slot in content.split(','):
                            if '=' not in slot:
                                continue
                            slot_name, slot_val = slot.split('=')
                            if slot_name == 'task':
                                continue
                            if '"' in slot_val:
                                slot_val = slot_val[1:-1]
                            # print('slot_val =', slot_val)
                            slot_len = len(slot_val.split())

                            replaced_field = ['_' + slot_name.upper()] * slot_len
                            trans = trans.replace(slot_val, ' '.join(replaced_field))

                    new_trans = [w if w[0] == '_' else '_' for w in trans.split()]
                    # for word in trans.split():
                    #     if word[0] != '_':

                    slots_list.append(' '.join(new_trans).replace('ly', ''))
                    # slots_list.append(trans)

with open('Z_train', 'w') as z_file:
    z_file.write('\n'.join(slots_list) + '\n')

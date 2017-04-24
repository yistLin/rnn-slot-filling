#!/usr/local/bin/python3
import sys
import os
import argparse
import numpy as np
from collections import defaultdict
from json import loads

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from keras.models import load_model

def main(pathname='./', testfilename=None, outputfilename=None):
    buckets = [4, 7, 10, 20]
    models = []
    for i in range(len(buckets)):
        models.append(load_model(os.path.join(pathname, 'model-%d.hdf5' % i)))
        models[i].summary()
        print('model-%d.hdf5 loaded' % i)

    # load dictionary
    with open(os.path.join(pathname, 'from.word2id.txt'), 'r') as x_dict_file:
        word2id = loads(x_dict_file.read())
        word2id = defaultdict(lambda: 1, word2id)
    with open(os.path.join(pathname, 'to.id2word.txt'), 'r') as y_dict_file:
        id2word = loads(y_dict_file.read())

    if testfilename:
        lines = []
        answers = []
        with open(testfilename, 'r') as testfile:
            for line in testfile:
                words = line.strip().split()
                ids = [word2id[x] for x in words]
                lines.append(ids)

        for line in lines:
            for bucket_id, bucket_size in enumerate(buckets):
                if len(line) < bucket_size:
                    source = line + [word2id['_PAD']] * (bucket_size - len(line))
                    source = np.array(source).reshape(1, bucket_size)
                    prediction = models[bucket_id].predict_classes(source, batch_size=1, verbose=0)
                    break
            else:
                continue

            answer = [id2word[x] for x in prediction[0]]
            answers.append(' '.join(answer[:len(line)]))

        with open(outputfilename, 'w') as outputfile:
            answers.append('')
            outputfile.write('\n'.join(answers))

    else:
        try:
            line = input('> ')
            while line:
                words = line.split()
                ids = [word2id[x] for x in words]

                for bucket_id, bucket_size in enumerate(buckets):
                    if len(ids) < bucket_size:
                        print('length of ids < %d' % bucket_size)
                        ids += [word2id['_PAD']] * (bucket_size - len(ids))
                        ids = np.array(ids).reshape(1, bucket_size)
                        prediction = models[bucket_id].predict_classes(ids, batch_size=1, verbose=0)
                        break
                else:
                    print('This length is not supported')
                    continue

                answer = [id2word[x] for x in prediction[0]]
                print('ids =', ids)
                print('prediction =', prediction[0])
                print('answer =', answer)
                line = input('> ')
        except EOFError:
            print('END of decoding')
            return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decoding strings by bucketing models')
    parser.add_argument('model_dir', help='specify where stores the models')
    parser.add_argument('--file', help='decode strings from a specific file')
    parser.add_argument('--output', help='output decoded sentences')
    args = parser.parse_args()

    print('Model directory is:', args.model_dir)

    if args.file:
        main(pathname=args.model_dir, testfilename=args.file, outputfilename=args.output)
    else:
        main(pathname=args.model_dir)

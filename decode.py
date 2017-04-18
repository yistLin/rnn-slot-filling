#!/usr/local/bin/python3
import sys
import numpy as np
from json import loads
from keras.models import load_model

def main():
    buckets = [4, 7, 10, 20]
    models = []
    for i in range(len(buckets)):
        models.append(load_model('model-%d.hdf5' % i))
        models[i].summary()
        print('model-%d.hdf5 loaded' % i)

    # load dictionary
    with open('from.word2id.txt', 'r') as x_dict_file:
        word2id = loads(x_dict_file.read())
    with open('to.id2word.txt', 'r') as y_dict_file:
        id2word = loads(y_dict_file.read())

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
    main()

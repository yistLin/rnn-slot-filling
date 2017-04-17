#!/usr/local/bin/python3
import sys
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, Merge, TimeDistributed, Bidirectional
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint

def read_data(filename):
    data = []
    word2id = {'_PAD': 0}
    id2word = ['_PAD']
    cnt = 1
    with open(filename, 'r') as f:
        for line in f:
            words = line[:-1].split()
            ids = []
            for word in words:
                if word not in word2id:
                    word2id[word] = cnt
                    id2word.append(word)
                    ids.append(cnt)
                    cnt += 1
                else:
                    ids.append(word2id[word])
            data.append(ids)

    return data, word2id, id2word

def train_model(datasets, validation_split=0.1):
    model = Sequential()
    model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(5, 10)))
    model.add(Bidirectional(LSTM(10)))
    model.add(Dense(5))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.1, decay=1e-5, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)

    model.summary()

    print("Train...")
    # model.fit([X_train, X_train],
    #         Y_train,
    #         batch_size=32,
    #         nb_epoch=5,
    #         validation_data=([X_test, X_test], Y_test),
    #         verbose=1,
    #         show_accuracy=True)

def main():
    buckets = [3, 6, 10, 20]
    x_data, x_dict, _ = read_data(sys.argv[1])
    y_data, _, y_dict = read_data(sys.argv[2])

    datasets = [[] for i in range(len(buckets))]
    for source_ids, target_ids in zip(x_data, y_data):
        for bucket_id, bucket_size in enumerate(buckets):
            if len(source_ids) < bucket_size:
                datasets[bucket_id].append((source_ids, target_ids))
                break

    from_size = len(x_dict)
    to_size = len(y_dict)
    for bucket_id, bucket_size in enumerate(buckets):
        print('dataset[%d] with length = %d, has %d' % (bucket_id, bucket_size, len(datasets[bucket_id])))

        for data_id, (from_ids, to_ids) in enumerate(datasets[bucket_id]):
            # append _PAD
            from_ids += [x_dict['_PAD']] * (bucket_size - len(from_ids))
            to_ids += [x_dict['_PAD']] * (bucket_size - len(to_ids))

            # transform to one-hot
            from_onehot = np.zeros(shape=(bucket_size, from_size))
            to_onehot = np.zeros(shape=(bucket_size, to_size))
            from_onehot[np.arange(bucket_size), from_ids] = 1
            to_onehot[np.arange(bucket_size), to_ids] = 1
            datasets[bucket_id][data_id] = (from_onehot, to_onehot)

    train_model(x_train)

if __name__ == '__main__':
    main()

#!/usr/local/bin/python3
import sys
import numpy as np
from json import dumps
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, Bidirectional, Embedding, TimeDistributed
from keras.callbacks import ModelCheckpoint

def read_data(filename):
    data = []
    word2id = {'_PAD': 0, '_UNK': '1'}
    id2word = ['_PAD', '_UNK']
    cnt = 2
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

def train_model(datasets, buckets, from_size=1000, to_size=100):
    embedding_size = 128
    models = []

    for bucket_id, dataset in enumerate(datasets):
        # stack model
        model = Sequential()
        model.add(Embedding(from_size, embedding_size, input_length=buckets[bucket_id]))
        model.add(Bidirectional(LSTM(128, return_sequences=True)))
        model.add(LSTM(to_size, return_sequences=True))
        model.add(TimeDistributed(Dense(to_size, activation='softmax')))

        # compile model
        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
        model.summary()

        # collect all models
        models.append(model)
        print('model %d with input_length =%3d built' % (bucket_id, buckets[bucket_id]))

    for bucket_id, dataset in enumerate(datasets):
        X_train, Y_train = zip(*dataset)
        X_train = list(X_train)
        Y_train = np.array(list(Y_train))
        checkpoint = ModelCheckpoint(
            'model-%d-{epoch:03d}-{val_acc:.2f}.hdf5' % bucket_id,
            monitor='val_acc',
            verbose=1,
            save_best_only=False,
            save_weights_only=False,
            mode='auto',
            period=5)
        models[bucket_id].fit(
            X_train,
            Y_train,
            batch_size=32,
            epochs=100,
            validation_split=0.1,
            verbose=1,
            callbacks=[checkpoint])
        models[bucket_id].save('model-%d.hdf5' % (bucket_id))

def main():
    buckets = [4, 7, 10, 20]
    x_data, x_word2id, _ = read_data(sys.argv[1])
    y_data, y_word2id, y_id2word = read_data(sys.argv[2])

    # dump dictionary
    with open('from.word2id.txt', 'w') as x_dict_file:
        x_dict_file.write(dumps(x_word2id))
    with open('to.id2word.txt', 'w') as y_dict_file:
        y_dict_file.write(dumps(y_id2word))

    datasets = [[] for i in range(len(buckets))]
    for source_ids, target_ids in zip(x_data, y_data):
        for bucket_id, bucket_size in enumerate(buckets):
            if len(source_ids) < bucket_size:
                datasets[bucket_id].append((source_ids, target_ids))
                break

    from_size = len(x_word2id)
    to_size = len(y_word2id)
    for bucket_id, bucket_size in enumerate(buckets):
        print('dataset[%d] with length = %d, has %d' % (bucket_id, bucket_size, len(datasets[bucket_id])))

        for data_id, (from_ids, to_ids) in enumerate(datasets[bucket_id]):
            # append _PAD
            from_ids += [x_word2id['_PAD']] * (bucket_size - len(from_ids))
            to_ids += [y_word2id['_PAD']] * (bucket_size - len(to_ids))

            # transform to one-hot
            # from_onehot = np.zeros(shape=(bucket_size, from_size))
            # from_onehot[np.arange(bucket_size), from_ids] = 1
            to_onehot = np.zeros(shape=(bucket_size, to_size))
            to_onehot[np.arange(bucket_size), to_ids] = 1
            datasets[bucket_id][data_id] = (from_ids, to_onehot)

    train_model(datasets, buckets, from_size=from_size, to_size=to_size)

if __name__ == '__main__':
    main()

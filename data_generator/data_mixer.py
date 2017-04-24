#!/usr/bin/env python3

import sys
import random

def read_data(filename1, filename2):
    file1 = open(filename1, 'r')
    file2 = open(filename2, 'r')

    return list(zip(file1, file2))

if __name__ == '__main__':
    data_o = read_data(sys.argv[1], sys.argv[2])
    data_g = read_data(sys.argv[3], sys.argv[4])

    temp = data_o + data_g
    random.shuffle(temp)
    x_data, y_data = zip(*temp)

    assert len(x_data) == len(y_data)
    print('origin data lines:', len(x_data))

    x_test = x_data[:10000]
    x_train = x_data[10000:]

    y_test = y_data[:10000]
    y_train = y_data[10000:]

    assert len(x_train) == len(y_train)
    print('train data lines:', len(x_train))
    assert len(x_test) == len(y_test)
    print('test data lines:', len(x_test))

    with open('X_train', 'w+') as f:
        f.writelines(x_train)
    with open('Y_train', 'w+') as f:
        f.writelines(y_train)
    with open('X_test', 'w+') as f:
        f.writelines(x_test)
    with open('Y_test', 'w+') as f:
        f.writelines(y_test)


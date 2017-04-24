#!/usr/bin/env python3

import sys

def read_data(filename1, filename2):
    file1 = open(filename1, 'r')
    file2 = open(filename2, 'r')

    return list(zip(file1, file2))

if __name__ == '__main__':
    data = read_data(sys.argv[1], sys.argv[2])

    total_words = 0
    total_errors = 0
    total_accuracy = 0.0
    for x, y in data:
        if x[-1] == '\n':
            x = x[:-1]
        if y[-1] == '\n':
            y = y[:-1]
        x = x.split()
        y = y.split()

        assert len(x) == len(y)

        errors = 0
        for a, b in zip(x, y):
            if a != b:
                errors += 1

        accuracy = (len(x) - errors) / len(x)

        total_errors += errors
        total_words += len(x)
        total_accuracy += accuracy

    print('Average accuracy:', total_accuracy / len(data))
    print('Total accuracy:', (total_words - total_errors) / total_words)

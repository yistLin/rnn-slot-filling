#!/usr/bin/env python3

import sys

def read_data(filename1, filename2):
    file1 = open(filename1, 'r')
    file2 = open(filename2, 'r')

    return list(zip(file1, file2))

def get_slots(data, slot):
    slots = set()
    for x, y in data:
        x = x.split(' ')
        y = y.split(' ')
        for index, word in enumerate(y):
            if word == slot:
                slots.add(x[index])

    return slots

if __name__ == '__main__':
    data = read_data(sys.argv[1], sys.argv[2])

    # slots = ['_', '_FOOD', '_AREA', '_PRICERANGE', '_NAME', '_TYPE']
    print(get_slots(data, '_FOOD'))
    print(get_slots(data, '_AREA'))
    print(get_slots(data, '_PRICERANGE'))
    print(get_slots(data, '_NAME'))

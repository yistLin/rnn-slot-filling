#!/usr/bin/env python3

import sys
import random

countrys = ['indonesian', 'german', 'french', 'persian', 'british', 'brazilian',
    'spanish', 'malaysian', 'asian', 'swiss', 'caribbean', 'korean', 'austrian',
    'italian', 'swedish', 'thai', 'english', 'singaporean', 'american',
    'african', 'scottish', 'belgian', 'turkish', 'mediterranean', 'vietnamese',
    'scandinavian', 'romanian', 'danish', 'european', 'polish', 'moroccan',
    'jamaican', 'indian', 'cuban', 'cantonese', 'australian', 'irish',
    'hungarian', 'mexican', 'greek', 'russian', 'portuguese', 'lebanese',
    'chinese', 'japanese']

adjectives = ['vegetarian', 'unusual', 'traditional', 'modern', 'creative',
    'international', 'fusion', 'nice', 'fine', 'good', 'bad', 'dirty']

foods = ['steak', 'pasta', 'canapes', 'fast food', 'ramen', 'chips',
    'french fries', 'chicken', 'fish', 'beef', 'beer', 'wine', 'whiskey',
    'turkey', 'curry', 'pizza', 'risotto', 'rice', 'noodles', 'coffee', 'juice',
    'tea', 'lemonade', 'omelette', 'brunch', 'cake', 'teppanyaki', 'seafood',
    'burger', 'salad', 'sushi']

restaurants = ['restaurant', 'cafe', 'pub']

areas = ['east', 'north', 'south', 'west', 'centre']

priceranges = ['expensive', 'moderate priced', 'cheap', 'moderately priced']

searchs = ['i want to find', 'im looking for']

serves = ['that serves', 'serving']

# _FOOD _FOOD
def country_food():
    x, y = [], []
    for country in countrys:
        x.append(country + ' food')
        y.append('_FOOD _FOOD')

    return x, y

# a/an _TYPE _TYPE
def a_adjective_type():
    x, y = [], []
    for adjective in adjectives:
        article = 'an' if (adjective[0] in ['a', 'e', 'i', 'o', 'u']) else 'a'
        for restaurant in restaurants:
            x.append(article + ' ' + adjective + ' ' + restaurant)
            y.append('_ _TYPE _TYPE')

    return x, y

# a/an _PRICERANGE _TYPE
def a_pricerange_type():
    x, y = [], []
    for pricerange in priceranges:
        article = 'an' if (pricerange[0] in ['a', 'e', 'i', 'o', 'u']) else 'a'
        for restaurant in restaurants:
            x.append(article + ' ' + pricerange + ' ' + restaurant)
            y.append('_ ' + '_PRICERANGE ' * len(pricerange.split()) + '_TYPE')

    return x, y

if __name__ == '__main__':
    x_data = []
    y_data = []

    # _FOOD
    for food in foods:
        x_data.append(food)
        y_data.append('_FOOD ' * len(food.split()))

    # _FOOD _FOOD
    x, y = country_food()
    x_data += x
    y_data += y

    # a/an _TYPE _TYPE
    x, y = a_adjective_type()
    x_data += x
    y_data += y

    # a/an _PRICERANGE _TYPE
    x, y = a_pricerange_type()
    x_data += x
    y_data += y

    # how about _FOOD _FOOD
    x_list, y_list = country_food()
    for x, y in zip(x_list, y_list):
        x_data.append('how about ' + x)
        y_data.append('_ _ ' + y)

    # _TYPE in the _AREA part of town
    for restaurant in restaurants:
        for area in areas:
            x_data.append(restaurant + ' in the ' + area + ' part of town')
            y_data.append('_TYPE _ _ _AREA _ _ _')

    # i want to find/im looking for a/an _PRICERANGE/_TYPE _TYPE
    for search in searchs:
        x_list_p, y_list_p = a_pricerange_type()
        x_list_a, y_list_a = a_adjective_type()
        for x, y in zip(x_list_p + x_list_a, y_list_p + y_list_a):
            x_data.append(search + ' ' + x)
            y_data.append('_ ' * len(search.split()) + y)

    # i want to find/im looking for a/an _PRICERANGE/_TYPE _TYPE in the _AREA part of town
    for search in searchs:
        x_list_p, y_list_p = a_pricerange_type()
        x_list_a, y_list_a = a_adjective_type()
        for x, y in zip(x_list_p + x_list_a, y_list_p + y_list_a):
            for area in areas:
                x_data.append(search + ' ' + x + ' in the ' + area + ' part of town')
                y_data.append('_ ' * len(search.split()) + y + ' _ _ _AREA _ _ _')

    # i want to find/im looking for a/an _PRICERANGE/_TYPE _TYPE that serves/serving _FOOD
    for search in searchs:
        x_list_p, y_list_p = a_pricerange_type()
        x_list_a, y_list_a = a_adjective_type()
        for x, y in zip(x_list_p + x_list_a, y_list_p + y_list_a):
            for serve in serves:
                for food in foods:
                    x_data.append(search + ' ' + x + ' ' + serve + ' ' + food)
                    y_data.append('_ ' * len(search.split()) + y + ' _' * len(serve.split()) + ' _FOOD' * len(food.split()))

    assert len(x_data) == len(y_data)

    temp = list(zip(x_data, y_data))
    random.shuffle(temp)
    x_data, y_data = zip(*temp)

    counts = [0, 0, 0, 0]
    buckets = [4, 7, 10, 20]
    for x, y in zip(x_data, y_data):
        for index, value in enumerate(buckets):
            if len(x.split()) < value:
                counts[index] += 1
                break

        print(x)
        print(y)

        assert len(x.split()) == len(y.split())

    print(counts)

    with open('X_g_data', 'w+') as f:
        f.write('\n'.join(x_data) + '\n')
    with open('Y_g_data', 'w+') as f:
        f.write('\n'.join(y_data) + '\n')


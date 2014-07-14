import itertools


def create_dict(list_keys, list_values):
    #return dict(zip(list_keys, list_values + [None for _ in range(len(list_keys) - len(list_values))]))
    d = dict(itertools.zip_longest(list_keys, list_values, fillvalue=None))
    if None in d:
        del d[None]
    return d


def create_dict_loop(list_keys, list_values):
    len_keys = len(list_keys)
    len_values = len(list_values)
    d = dict()
    for i in range(min(len_keys, len_values)):
        d[list_keys[i]] = list_values[i]
    return d
# Basic functional programming tools.
# Note: These work slightly differently then Python's functools
# Note: None of these functions change the original list

import numpy as np


# creates a list of items from original that satisfy the predicate
# is_even = lambda x: x % 2 == 0
# filter(is_even, [2, 3, 4, 5, 6]) = [2, 4, 6]
def filter(pred, lst):
    return_value = []
    for x in lst:
        if pred(x):
            return_value.append(x)
    return return_value

# creates a list of outputs from original list
# f = lambda x: 2*x
# map(f, [2 3 4]) = [4, 6, 8]
def map(fn, lst):
    return_value = []
    for x in lst:
        return_value.append(fn(x))
    return return_value

# returns True if every element of the list satisfies pred, False otherwise
# is_even = lambda x: x % 2 == 0
# every(is_even, [2, 3, 4]) = False
# every(is_even, [2, 4, 6]) = True
def every(pred, list):
    for x in list:
        if not pred(x):
            return False
    else:
        return True

# returns True of some element of the list satisfied pred, False otherwise
# some(is_even, [2, 3, 4]) = True
# some(is_even, [3, 5, 7]) = False
def some(pred, list):
    for x in list:
        if pred(x):
            return True
    else:
        return False


# returns source_list with items_to_remove removed.
# remove_from_list([1, 2, 3, 4, 5], [1, 3, 4]) = [2, 5]
def remove_from_list(source_list, items_to_remove):
    return [s for s in source_list if not s in items_to_remove]
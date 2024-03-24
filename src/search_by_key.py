import os.path
import random
import time
import matplotlib.pyplot as plt
import math

from typing import List

from TreeNode import BinarySearchTree
from Flight import *


# Потемин Дмитрий Иванович СКБ 211
# сортировки: пузырьком, шейкером, быстрой сортировкой

def show_time(func, arg, initalize, name) -> (float, float):
    """
    Estimates time to process function

    :param func: function to use
    :param arg: arg to process
    :param initalize: initializer of search object
    :param name: name of function to show information
    :rtype: value of estimated function and time to process it
    """
    rec = initalize(arg)
    start_time = time.time()
    retv = func(rec, arg)
    end_time = time.time() - start_time
    return retv, end_time


def initialize_btree(ll: List[Flight]) -> BinarySearchTree:
    """
    :param ll: list of flights
    :rtype: BinarySearchTree initialized
    """
    a = BinarySearchTree()
    for i in ll:
        a.insert(i.airline, i)
    return a


def btree(a: BinarySearchTree, ll: List[Flight]):
    """
    Search with btree

    :param a: initialized binary search tree
    :param ll: list of flights
    """
    it = random.choices(ll, k=10)
    for i in it:
        a.find(i.airline)
    return


def initialize_multimap(ll: List[Flight]) -> dict:
    """
    Intialized multimap

    :param ll: list of flights
    :return:  dictionary
    """
    a = dict()
    for i in ll:
        bb = a.get(i.airline, None)
        if bb is None:
            a[i.airline] = [i]
        else:
            a[i.airline] += [i]
    return a


def multimap(a: dict, ll: List[Flight]):
    """
    Searches with multimap

    :param a: dictionary
    :param ll: list of flights
    """
    it = random.choices(ll, k=10)
    for i in it:
        a[i.airline]


def main():
    flights2 = load_flights_from_csv(os.path.abspath("src/flights.csv"))
    sizes = [100, 500, 1000, 2000, 3000, 6000, 7000, 8000, 100000, 200000]
    times_b = []
    times_m = []
    for i in sizes:
        print(i)
        flights = random.sample(flights2, i)
        find_flights_btree, end_time_btree = show_time(btree, flights.copy(), initialize_btree, "Bubble")
        find_flights_multimap, end_time_multimap = show_time(multimap, flights.copy(), initialize_multimap, "Multimap")
        times_m.append(math.log(end_time_multimap))
        times_b.append(math.log(end_time_btree))
    plt.plot(sizes, times_b, label="Btree")
    plt.plot(sizes, times_m, label="Multimap")
    plt.xlabel("Length of list (number)")
    plt.ylabel("Time taken (seconds)")
    plt.legend(loc="upper left")
    plt.savefig("select.png")


if __name__ == '__main__':
    main()

import os.path
import random
import time

from Flight import *
import matplotlib.pyplot as plt
import math


# Потемин Дмитрий Иванович СКБ 211
# поиск: BinaryTree




def show_time(func, arg, name) -> (float, float):
    """
    Estimates time to process function

    :param func: function to use
    :param arg: arg to process
    :param name: name of function to show information
    :return: value of estimated function and time to process it
    """
    start_time = time.time()
    retv = func(arg)
    end_time = time.time() - start_time
    return retv, end_time


def main():
    flights2 = load_flights_from_csv(os.path.abspath("src/flights.csv"))
    sizes = [100, 500, 1000, 2000, 3000, 6000, 7000, 8000, 100000, 200000]
    times_b = []
    times_c = []
    times_q = []
    for i in sizes:
        print(i)
        flights = random.sample(flights2, i)
        sorted_flights_bubble, end_time_bubble = show_time(bubble_sort, flights.copy(), "Bubble")
        sorted_flights_cocktail, end_time_cocktail = show_time(cocktail_sort, flights.copy(), "Cocktail")
        sorted_flights_quick, end_time_quick = show_time(quick_sort, flights.copy(), "Quick")
        times_b.append(math.log(end_time_bubble))
        times_c.append(math.log(end_time_cocktail))
        times_q.append(math.log(end_time_quick))
        write_csv("sorts/Bubble_{}".format(i), sorted_flights_bubble)
        write_csv("sorts/Cocktail_{}".format(i), sorted_flights_cocktail)
        write_csv("sorts/Quick_{}".format(i), sorted_flights_quick)
        print("finished")
    plt.plot(sizes, times_b, label="Bubble")
    plt.plot(sizes, times_c, label="Cocktail")
    plt.plot(sizes, times_q, label="Quick")
    plt.xlabel("Length of list (number)")
    plt.ylabel("Time taken (seconds)")
    plt.legend(loc="upper left")
    plt.savefig("sorts.png")


if __name__ == '__main__':
    main()

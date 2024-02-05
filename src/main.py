import csv
import datetime
import os.path
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import math

# Потемин Дмитрий Иванович СКБ 211
# сортировки: пузырьком, шейкером, быстрой сортировкой
class Flight:
    def __init__(self, dictionary):
        """
        Initializes object from dict
        :param dictionary: dict
        """
        self.arrival_time = dictionary['arrival_time']
        self.arrival_date = dictionary['arrival_date']
        self.airline = dictionary['airline']
        self.passengers = dictionary['passengers']
        self.flight_number = dictionary['flight_number']

    def __lt__(self, flight2):
        """
        Custom comparator function
        :param flight2: second comparable object
        :return: bool -- True if self is less than flight2
        """
        if self.arrival_date < flight2.arrival_date:
            return True
        elif self.arrival_date > flight2.arrival_date:
            return False
        if self.arrival_time < flight2.arrival_time:
            return True
        elif self.arrival_time > flight2.arrival_time:
            return False
        if self.airline < flight2.airline:
            return True
        elif self.airline > flight2.airline:
            return False
        return self.passengers > flight2.passengers

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __eq__(self, other):
        return (self.arrival_date == other.arrival_date and
                self.arrival_time == other.arrival_time and
                self.airline == other.airline and
                self.passengers == other.passengers)
    def __repr__(self):
        """
        Representation of flight
        :return: string of represented object
        """
        return "{} {} {} {} {}".format(self.flight_number, self.airline, self.passengers, self.arrival_date,
                                       self.arrival_time)


def bubble_sort(flights):
    """
    Simple buble sort
    :param flights: list of sortable objects
    :return: sorted list
    """
    n = len(flights)
    for i in range(n):
        for j in range(0, n - i - 1):
            if not (flights[j] < flights[j + 1]):
                flights[j], flights[j + 1] = flights[j + 1], flights[j]
    return flights


def cocktail_sort(flights):
    """
    Cocktail sort for given list
    :param flights: list of sortable objects
    :return: sorted list
    """
    n = len(flights)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if not (flights[i] < flights[i + 1]):
                flights[i], flights[i + 1] = flights[i + 1], flights[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if not (flights[i] < flights[i + 1]):
                flights[i], flights[i + 1] = flights[i + 1], flights[i]
                swapped = True
        start += 1
    return flights


def quick_sort(flights):
    """
    Quick sorts given list
    :param flights: list of sortable objects
    :return: sorted object list
    """
    if len(flights) <= 1:
        return flights
    else:
        pivot = flights[len(flights) // 2]
        left = [x for x in flights if (x < pivot)]
        middle = [x for x in flights if not (x < pivot) and not (pivot < x)]
        right = [x for x in flights if (pivot < x)]
        return quick_sort(left) + middle + quick_sort(right)


def parse_time(t):
    """
    Parses time from "0000" format
    :param t: string to parse
    :return: parsed datetime object
    """
    if pd.isnull(t) or t == "":
        return None
    else:
        t = str(int(float(t))).zfill(4)  # Дополняем строку до 4 символов, добавляя нули слева
        try:
            return datetime.datetime.strptime(t, "%H%M").time()
        except ValueError as e:
            return None


def load_flights_from_csv(file_path):
    """
    Loads flights from file_path
    :param file_path: path to load from csv
    :return: List of Flight objects initialized from dicts
    """
    flights1 = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if not all(key in row for key in ["year", "month", "day", "arr_time", "carrier", "flight"]):
                continue
            time = parse_time(row["arr_time"])
            if time is not None:
                flight_data = {
                    "flight_number": row["flight"],
                    "airline": row["carrier"],
                    "arrival_date": datetime.datetime(int(row["year"]), int(row["month"]), int(row["day"])).date(),
                    "arrival_time": time,
                    "passengers": int(row["distance"])
                }
                flights1.append(Flight(flight_data))
    return flights1


def write_csv(name, rows):
    """
    Write csv file with Flights named "{Name}.csv
    :param name: Name of sort or file
    :param rows: Rows to write
    """
    with open(name + ".csv", mode='w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=vars(rows[0]).keys())
        csv_writer.writeheader()
        csv_writer.writerows(map(vars, rows))


def show_time(func, arg, name):
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
    plt.plot(sizes, times_b, label="Bubble")
    plt.plot(sizes, times_c, label="Cocktail")
    plt.plot(sizes, times_q, label="Quick")
    plt.xlabel("Length of list (number)")
    plt.ylabel("Time taken (seconds)")
    plt.legend(loc="upper left")
    plt.savefig("sorts.png")
if __name__ == '__main__':
    main()

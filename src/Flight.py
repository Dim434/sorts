import csv
import datetime
from typing import List


class Flight:
    def __init__(
            self,
            arrival_time: int,
            arrival_date: int,
            airline: str,
            passengers: int,
            flight_number: str
    ):
        """
        Initializes object from dict

        :param arrival_date: date of arrival
        :param arrival_time: time of arrival
        :param airline: airline
        :param passengers: count passengers
        :param flight_number: flight number
        """
        self.arrival_time = arrival_time
        self.arrival_date = arrival_date
        self.airline = airline
        self.passengers = passengers
        self.flight_number = flight_number

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


def bubble_sort(flights: List[Flight]) -> List[Flight]:
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


def cocktail_sort(flights: List[Flight]) -> List[Flight]:
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


def quick_sort(flights: List[Flight]) -> List[Flight]:
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


def datetime_to_int(dt) -> int:
    return int(dt.strftime("%Y%m%d%H%M%S"))


def parse_time(t: str):
    """
    Parses time from "0000" format

    :param t: string to parse
    :return: parsed datetime object
    """
    if t is None or t == "":
        return None
    else:
        t = str(int(float(t))).zfill(4)  # Дополняем строку до 4 символов, добавляя нули слева
        try:
            return datetime_to_int(datetime.datetime.strptime(t, "%H%M"))
        except ValueError as e:
            return None


def load_flights_from_csv(file_path: str) -> List[Flight]:
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
                    "arrival_date": int(
                        datetime.datetime(int(row["year"]), int(row["month"]), int(row["day"])).strftime('%Y%m%d')),
                    "arrival_time": time,
                    "passengers": int(row["distance"])
                }
                flights1.append(
                    Flight(
                        arrival_date=int(
                            datetime.datetime(int(row["year"]), int(row["month"]), int(row["day"])).strftime('%Y%m%d')),
                        arrival_time=time,
                        passengers=flight_data['passengers'],
                        airline=flight_data['airline'],
                        flight_number=flight_data['flight_number']
                    )
                )
    return flights1


def write_csv(name: str, rows: List[Flight]):
    """
    Write csv file with Flights named "{Name}.csv

    :param name: Name of sort or file
    :param rows: Rows to write
    """
    with open(name + ".csv", mode='w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['flight_number', 'airline', 'passengers', 'arrival_date',
                                                          'arrival_time'])
        csv_writer.writeheader()
        csv_writer.writerows(
            map(lambda x: {'flight_number': x.flight_number,
                           'airline': x.airline,
                           'passengers': x.passengers,
                           'arrival_date': x.arrival_date,
                           'arrival_time': x.arrival_time},
                rows
                )
        )
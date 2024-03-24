from typing import List

from Flight import Flight


class TreeNode:
    def __init__(self, key: str, flight: Flight):
        """
        Initialize tree node

        :param key: key to search
        :param flight: flight to insert
        """
        self.key = key
        self.flights = [flight]
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key: str, flight: Flight):
        """
        Inserts a flight into binarySearch tree with key

        :param key: Key to use
        :param flight: Flight to insert
        """
        if not self.root:
            self.root = TreeNode(key, flight)
        else:
            self._insert_recursive(self.root, key, flight)

    def _insert_recursive(self, node: TreeNode, key: str, flight: Flight):
        """
        Inserts recuresively

        :param node: Node
        :param key: Key
        :param flight: Flight
        """
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, flight)
            else:
                self._insert_recursive(node.left, key, flight)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, flight)
            else:
                self._insert_recursive(node.right, key, flight)
        else:  # Equal keys, add flight to the flights list
            node.flights.append(flight)

    def find(self, key: str) -> List[Flight]:
        """
        Find values with key

        :param key: key to search
        :return: Flights
        """
        return self._find_recursive(self.root, key)

    def _find_recursive(self, node: TreeNode, key: str) -> List[Flight]:
        """
        Search recursively by key

        :param node: Node to search through
        :param key: Key to search
        :return: Flights or No flights
        """
        if node is None:
            return None
        elif key < node.key:
            return self._find_recursive(node.left, key)
        elif key > node.key:
            return self._find_recursive(node.right, key)
        else:
            return node.flights

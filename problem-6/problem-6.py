#!/usr/bin/env python3

"""Problem 6 of the Data Structures Project.

Notes:
    1. This code could have been simplified by using the builtin Python set Type and the union and intersection
        operations. They weren't used to illustrate the basic functionality.

Assumptions:
    1. Duplicates in the input lists are ignored, therefore no duplicates in the union and intersection output.
    2. Order of the linked lists does not need to be maintained.
"""

from __future__ import annotations
from datetime import datetime
import hashlib
from time import time


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def __len__(self):
        return self.size

    def get_unique_values(self) -> list:
        """Return the unique values of the linked list.

        Returns:
            list: The unique values in the linked list.
        """
        values = []
        node = self.head
        while node:
            if node.value not in values:
                values.append(node.value)
            node = node.next
        return values


def intersection(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """Generates a new Linked List that is the intersection of the two input Linked lists.

    Note: Duplicates in the input lists are ignores and order is not maintained so:
        [1, 1, 2, 3, 3] intersection [2, 2, 2, 3] = [2, 3] or [3, 2]

    Args:
        list1 (LinkedList): The first linked list to process.
        list2 (LinkedList): The second linked list to process.

    Returns:
        LinkedList: The union of the two input linked lists.
    """
    unique_values1 = list1.get_unique_values()
    unique_values2 = list2.get_unique_values()
    new_list = LinkedList()
    for v in [v for v in unique_values1 if v in unique_values2]:
        new_list.append(v)

    return new_list


def union(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """Generates a new Linked List that is the union of the two input Linked lists.

    Note: Duplicates in the input lists are ignores and order is not maintained so:
        [1, 1, 1] union [2, 2, 2] = [1, 2] or [2, 1]

    Args:
        list1 (LinkedList): The first linked list to process.
        list2 (LinkedList): The second linked list to process.

    Returns:
        LinkedList: The union of the two input linked lists.
    """
    new_list = LinkedList()
    unique_values1 = list1.get_unique_values()
    for v in unique_values1:
        new_list.append(v)
    for v in [v for v in list2.get_unique_values() if v not in unique_values1]:
        new_list.append(v)

    return new_list


def given_tests():

    test = 0
    for element_1, element_2 in [([3, 2, 4, 35, 6, 65, 6, 4, 3, 21], [6, 32, 4, 9, 6, 1, 11, 21, 1]),
                                 ([3, 2, 4, 35, 6, 65, 6, 4, 3, 23], [1, 7, 8, 9, 11, 21, 1])]:
        test += 1
        print(f"\nGiven test {test}")

        linked_list_1 = LinkedList()
        for i in element_1:
            linked_list_1.append(i)

        linked_list_2 = LinkedList()
        for i in element_2:
            linked_list_2.append(i)

        print(f"List 1: {linked_list_1}")
        print(f"List 2: {linked_list_2}")

        # Check the union function
        actual = union(linked_list_1, linked_list_2)
        expected = set(element_1).union(element_2)
        print(f"\nUnion: {actual}")
        errors = expected.symmetric_difference(actual.get_unique_values())
        if len(errors) == 0:
            print(f"Test {test} union correct, expected and actual values are the same.\n")
        else:
            print(f"Error test {test}: errors = {errors}.\n")

        # Check the intersection function
        actual = intersection(linked_list_1, linked_list_2)
        expected = set(element_1).intersection(element_2)
        print(f"Intersection: {actual}")
        errors = expected.symmetric_difference(actual.get_unique_values())
        if len(errors) == 0:
            print(f"Test {test} intersection, expected and actual values are the same.\n")
        else:
            print(f"Error test {test}: errors = {errors}.\n")


# noinspection PyBroadException
def user_tests():
    """Runs the user tests."""

    # Set some testing constants
    n_errors = 0

    # Check the BlockChain print functionality
    print("\nUser test set 1 - print functionality.")
    test = 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.\n")
    else:
        print("WOO HOO, No errors detected.\n")


# **********************************************************
if __name__ == '__main__':
    given_tests()
    user_tests()

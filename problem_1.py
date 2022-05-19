#!/usr/bin/env python3

from time import time

"""Problem 1 of the Data Structures Project.

Assumptions:
    1. Both the key and value of the cache must be integers.
    2. 'Use' is defined as both 'set' and 'get' access, e.i. both methods place the node at the head of the Cache. 
    3. The most recently used node is placed at the head of the Doubly Linked List (Cache).
    4. A capacity less than 2 is not valid, as it would be degenerate.
"""


class DoubleNode:
    """The Double Node Class used to track the Node's key, value pair plus previous and next node order by use.

    Attributes:
        key (int): The node's value with is also the key to the map in the LRU_Cache.
        value (int): The node's value.
        next (Node): The closest node that is least recently used.
        previous (Node): The closest node that is more recently used.
    """

    def __init__(self, key: int, value: int):
        """The object initialization method.

        Args:
            key (int): The node's key with is also the key to the map in the LRU_Cache.
            value (int): The node's value.
        """

        # Check arguments
        if not isinstance(key, int):
            raise AttributeError("The key must be an integer.")
        if not isinstance(value, int):
            raise AttributeError("The value must be an integer.")

        # Set attributes
        self.key = key
        self.value = value
        self.next = None
        self.previous = None


class LRU_Cache(object):
    """The Least Recently Used (LRU) Cache.

    Notes:
     - The key and value of the Cache must be integers.
     - The maximum size of the Cache is limited to the capacity defined on initialization.
     - If the capacity is exceeded, the least recently used Cache element is deleted.
     - If the key passed to the get method does not exist, -1 is returned.

    Attributes:
        capacity (int): The maximum size of the cache, i.e. maximum n_elements.
        n_elements (int): The number of elements saved in the cache.
        map (dict of DoubleNode): The map containing the actual cache data saved in a Double Node.
    """

    def __init__(self, capacity: int = 5):
        """The object initialization method.

        Args:
            capacity (int): The maximum size of the cache, which must be greater than 1.

        Raises:
            AttributeError: If the given capacity is not an integer greater than 1.
        """

        # Check the given capacity
        if not isinstance(capacity, int):
            raise AttributeError("Given capacity must be an integer.")
        if capacity <= 1:
            raise AttributeError(f"Given capacity of {capacity} must be greater than 1.")

        # Initialize class variables
        self.capacity = capacity
        self.n_elements = 0
        self.map = {}
        self.head = None
        self.tail = None

    def get(self, key: int) -> int:
        """Return the value of the given key or -1 if it doesn't exist.

        Raises:
            AttributeError: If the requested key is not an int.
        """

        # Check that the requested key is an integer
        if not isinstance(key, int):
            raise AttributeError("The requested key must be an int.")

        # Get the value with a default value of -1 if the key doesn't exist
        node = self.map.get(key, -1)
        if node == -1:
            return node

        # Update the LRU queue if the node exists
        value = node.value
        current_previous = node.previous
        current_next = node.next

        # If node is already at the head, there is nothing to do
        if current_previous is None:
            return value

        # Update the head
        current_head = self.head
        self.head = node
        self.head.previous = None
        self.head.next = current_head
        current_head.previous = self.head

        # If node is at the tail, the tail needs to be updated
        if current_next is None:
            self.tail = current_previous
            self.tail.next = None

        # Move the node to the head of the doubly linked list
        else:
            current_previous.next = current_next
            current_next.previous = current_previous

        return value

    def print_cache(self):
        """Helper method to prent the Cache during debugging."""

        print("\nForward traverse through the Cache.")
        node = self.head
        while node:
            print(f"key = {node.key}, value = {node.value}")
            node = node.next

        print("\nReverse traverse through the Cache.")
        node = self.tail
        while node:
            print(f"key = {node.key}, value = {node.value}")
            node = node.previous
        print("")

    def set(self, key: int, value: int):
        """Set the value if the key is not present in the cache. If the cache is at capacity remove the oldest item.

        Args:
            key (int): The key to set, which will be the key in the internal map pointing to the associated node.
            value (int): The value to set, which will be the associated node's value.
        """

        # Check arguments
        if not isinstance(key, int):
            raise AttributeError("The key must be an integer.")
        if not isinstance(value, int):
            raise AttributeError("The value must be an integer.")

        # Remove the node from the doubly linked list if it exists
        # -------------------------------------------------------------------------------
        node = self.map.get(key, -1)
        if node != -1:
            # Special case when the node is already at the head
            if node.previous is None:
                node.value = value
                return

            # Special case when the node is already at the tail, just update the tail
            if node.next is None:
                self.tail = node.previous
                self.tail.next = None

            # Standard interior node removal
            else:
                node.previous.next = node.next
                node.next.previous = node.previous
            self.n_elements -= 1

        # Make a new node, add it to the map and place it at the head of the doubly linked list
        new_node = DoubleNode(key=key, value=value)
        self.map[key] = new_node
        self.n_elements += 1
        current_head = self.head
        self.head = new_node
        self.head.next = current_head

        # Update the previous head's previous pointer
        if self.n_elements > 1:
            self.head.next.previous = self.head

        # Set the tail if now have two elements
        if self.n_elements == 2:
            self.tail = current_head
            self.tail.previous = self.head

        # Delete the least used node if already at capacity
        if self.n_elements > self.capacity:
            current_tail = self.tail
            del self.map[current_tail.key]
            current_tail.previous.next = None
            self.tail = current_tail.previous


# **********************************************************
if __name__ == '__main__':

    # First set of given tests
    print("\nGiven set of tests")
    n_errors = 0
    our_cache = LRU_Cache(5)
    our_cache.set(1, 1)
    our_cache.set(2, 2)
    our_cache.set(3, 3)
    our_cache.set(4, 4)

    test = 0
    for arg, expected in [(1, 1), (2, 2), (9, -1)]:
        test += 1
        actual = our_cache.get(arg)
        if expected == actual:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    # Second set of given tests
    our_cache.set(5, 5)
    our_cache.set(6, 6)
    for arg, expected in [(3, -1)]:
        test += 1
        actual = our_cache.get(arg)
        if expected == actual:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    # Add your own test cases: include at least three test cases
    # and two of them must include edge cases, such as null, empty or very large values

    # User Test Case 1 - Error handling on LRU Cache instantiation
    print("\nUser test set 1 - Error handling on LRU Cache instantiation")
    test = 0
    for arg in [-1, 0, 1, 3.5, "4", []]:
        test += 1
        try:
            our_cache = LRU_Cache(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User Test Case 2 - Error handling on DoubleNode instantiation
    print("\nUser test set 2 - Error handling on DoubleNode instantiation")
    test = 0
    for args in [(1, ""), ("2", 2), ("", []), (10.2, 3)]:
        test += 1
        try:
            DoubleNode(args[0], args[1])
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User Test Case 3 - Error handling on get method
    print("\nUser test set 3 - Error handling on get method")
    test = 0
    our_cache = LRU_Cache(2)
    for arg in ["", "2", [], {}]:
        test += 1
        try:
            # noinspection PyTypeChecker
            our_cache.get(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User Test Case 4 - Error handling on set method
    print("\nUser test set 4 - Error handling on set method")
    test = 0
    our_cache = LRU_Cache(2)
    for args in [(1, ""), ("2", 2), ("", []), (10.2, 3), (10, None)]:
        test += 1
        try:
            # noinspection PyTypeChecker
            our_cache.set(args[0], args[1])
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User Test Case 5.1 - get from an empty Cache
    print("\nUser test set 5 - Edge cases")
    test = 0
    our_cache = LRU_Cache(10)
    test += 1
    actual = our_cache.get(3)
    if actual == -1:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected -1 but got {actual}.")
        n_errors += 1

    # User Test Case 5.2 - add the same key many times with different values and verify that the last value was saved
    our_cache = LRU_Cache(2)
    test += 1
    for i in range(10):
        our_cache.set(2, i)
    actual = our_cache.get(2)
    if actual == 9:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected 9 but got {actual}.")
        n_errors += 1

    # User Test Case 5.3 - Continuation of previous case
    #    Add a different key many times to ensure only one element was added to Cache
    test += 1
    for i in range(5):
        our_cache.set(3, i)
    actual = our_cache.get(2)
    if actual == 9:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected 9 but got {actual}.")
        n_errors += 1

    # User Test Case 5.4 - Continuation of previous case
    #    Add a key and verify 2 still exists, this means the get operation placed it at the head (capacity = 2)
    test += 1
    our_cache.set(4, 0)
    actual = our_cache.get(2)
    if actual == 9:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected 9 but got {actual}.")
        n_errors += 1

    # User Test Case 5.5 - Continuation of previous case
    #    Verify Cache contents
    #    Add 2 values and verify previous keys no longer exist, this verifies the capacity = 2 works (cache = [4, 5])
    for arg, expected in [(2, 9), (4, 0), (1, -1), (3, -1)]:
        test += 1
        actual = our_cache.get(arg)
        if actual == expected:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    # We know from above that 1 and 3 do not exist, so they should push 2 and 4 out of the cache
    our_cache.set(key=1, value=10)
    our_cache.set(key=3, value=30)
    for arg, expected in [(2, -1), (4, -1), (1, 10), (3, 30)]:
        test += 1
        actual = our_cache.get(arg)
        if actual == expected:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    # User Test Case 5.6 - Previously capacity = 2, which is a special case, this checks the cache with capacity = 3.
    #    Add two new values and verify 2 and 3 no longer exist, this verifies the capacity = 2 works (cache = [4, 5])
    our_cache = LRU_Cache(3)
    for k in range(5):
        our_cache.set(key=k, value=k*10)
    for arg, expected in [(0, -1), (1, -1), (2, 20), (3, 30), (4, 40)]:
        test += 1
        actual = our_cache.get(arg)
        if actual == expected:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    # User Test Case 5.7 - Let's check the scalability (time complexity)
    n_values = [10 ** i for i in range(1, 7)]
    get_times = []
    set_times = []
    for c in n_values:
        our_cache = LRU_Cache(c)
        for i in range(c):
            our_cache.set(key=i, value=i)

        start_time = time()
        our_cache.set(key=c+1, value=c+1)
        set_times.append(time() - start_time)

        start_time = time()
        our_cache.get(key=c + 1)
        get_times.append(time() - start_time)
    print(f"Capacity (n) = {n_values}")
    print(f"Get Times = {get_times}")
    print(f"Set Times = {set_times}")

    test += 1
    if abs(get_times[0] - get_times[-1]) < 0.0001:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: get method didn't have a constant time complexity.")
        n_errors += 1

    test += 1
    if abs(set_times[0] - set_times[-1]) < 0.0001:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: set method didn't have a constant time complexity.")
        n_errors += 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.")
    else:
        print("WOO HOO, No errors detected.")

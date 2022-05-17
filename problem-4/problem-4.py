#!/usr/bin/env python3

"""Problem 4 of the Data Structures Project.

This code searches for a user in a group/user hierarchy and returns True if found and false otherwise.

The group/user hierarchy is effectively a tree structure where each group is a node anf the users are the values in each
node.  Therefore, this is a tree search task.

I will implement the Breath First Search (BFS) algorithm to perform the search. For the search queue, I'll use a simple
list.

Notes:
    1. This code was tested with Python 3.10 and uses __future__ annotations for hinting within the Group class.

Assumptions:
    1. Duplicate user and group names are acceptable.

"""

from __future__ import annotations
from time import time


class Queue(object):
    """Simple search queue based on a list.

    Attributes:
        q (list): The queue of nodes to search.
    """
    def __init__(self):
        self.q = list()

    def enq(self, value):
        self.q.append(value)

    def deq(self):
        if len(self.q) > 0:
            return self.q.pop()
        else:
            return None

    def __len__(self):
        return len(self.q)


class Group(object):
    """The group objects, which are effective nodes of the tree.

    Attributes:
        name (str): The group name.
        groups (list of Group): The child groups (nodes).
        users (str): The user names of the current group.
    """
    def __init__(self, _name: str):
        """The object instantiation method.

        Args:
            _name (str): The group name.

        Raises:
            AttributeError: If the _name is not a string.
        """

        # Check argument
        if not isinstance(_name, str):
            raise AttributeError(f"Group name must be a string but {type(_name)} was given.")

        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group: Group):
        """Adds the child group to the current group.

        Args:
            group (Group): A child group to add to the current group.

        Raises:
            AttributeError: If the child "group" is not a Group object.
        """

        # Check argument
        if not isinstance(group, Group):
            raise AttributeError(f"Group name must be a Group object but {type(group)} was given.")

        self.groups.append(group)

    def add_user(self, user):
        """Adds the user to the group.

        Args:
            user (str): The user name.

        Raises:
            AttributeError: If the "user" name is not a string.
        """

        # Check argument
        if not isinstance(user, str):
            raise AttributeError(f"'user' must be a string but {type(user)} was given.")

        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name


def is_user_in_group(user: str, group: Group) -> bool:
    """Return True if user is in the group, False otherwise.

    Args:
        user(str): User name/id.
        group(class:Group): Group to check user membership against.

    Returns:
        bool: True if the user is found.

    Raises:
        AttributeError: If the "user" name is not a string.
        AttributeError: If the child "group" is not a Group object.
    """

    # Check arguments
    if not isinstance(user, str):
        raise AttributeError(f"'user' must be a string but {type(user)} was given.")
    if not isinstance(group, Group):
        raise AttributeError(f"Group name must be a Group object but {type(group)} was given.")

    # Initialize the queue with the root node
    search_queue = Queue()
    search_queue.enq(group)

    while len(search_queue) > 0:

        # Pull a node (group) from the search queue
        node = search_queue.deq()

        # Check for user in current group
        if user in node.get_users():
            return True

        # If user not in this group, add the children to the search queue
        for child in node.get_groups():
            search_queue.enq(child)

    # If you get here all the groups have been searched without finding the user, so return false
    return False


def given_tests():
    """Runs the given tests."""

    parent = Group("parent")
    child = Group("child")
    sub_child = Group("subchild")

    sub_child_user = "sub_child_user"
    sub_child.add_user(sub_child_user)

    child.add_group(sub_child)
    parent.add_group(child)

    if is_user_in_group(group=parent, user=sub_child_user):
        print(f"Given test 1 passed.")
    else:
        print(f"Error given test 1: {sub_child_user} not found.")

    if is_user_in_group(group=parent, user='foobar'):
        print(f"Error given test 2: `foobar` should return False.")
    else:
        print(f"Given test 2 passed.")


# noinspection PyBroadException
def user_tests():
    """Runs the user tests."""

    # Set some testing constants
    n_errors = 0

    # Test invalid arguments
    print("\nUser test set 1 - Invalid arguments.")
    test = 0
    good_group = Group('Atreides')
    for arg in [1, [], {}, None]:
        test += 1
        try:
            # noinspection PyTypeChecker
            Group(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

        test += 1
        try:
            # noinspection PyTypeChecker
            good_group.add_user(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

        test += 1
        try:
            # noinspection PyTypeChecker
            good_group.add_group(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    test += 1
    try:
        # noinspection PyTypeChecker
        good_group.add_group("Harkonnen")
    except AttributeError:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected an AttributeError exception.")
        n_errors += 1

    # Test invalid arguments
    print("\nUser test set 2 - Repeated group and user names.")
    test = 0
    top = Group('Atreides')
    top.add_user('Leto')
    parent = top
    for _ in range(10):
        child = Group('Atreides')
        child.add_user("Paul")
        parent.add_group(child)
        parent = child
    test += 1
    if is_user_in_group(user='Leto', group=top):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: 'Leto' not in top group.")
        n_errors += 1

    test += 1
    if not is_user_in_group(user='Leto', group=parent):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: 'Leto' should be in the lower groups.")
        n_errors += 1

    # Test an empty group
    print("\nUser test set 3 - Check a group structure with no users.")
    test = 0
    top = Group('Atreides')
    parent = top
    for _ in range(10):
        child = Group('Atreides')
        parent.add_group(child)
        parent = child
    test += 1
    if not is_user_in_group(user='Leto', group=top):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: group should be empty.")
        n_errors += 1

    # Test a structure with 1000 groups and users
    print("\nUser test set 4 - Large structure with a million groups, with one user per group.")
    test = 0
    top = Group('g0')
    parent = top
    n = 1000000
    start_time = time()
    for g in range(1, n+1):
        child = Group(f'g{g}')
        child.add_user(f'u{g}')
        parent.add_group(child)
        parent = child
    print(f"{time() - start_time:.2f} seconds to create the group.")
    test += 1
    start_time = time()
    if is_user_in_group(user=f'u{n}', group=top):
        print(f"Test {test} passed; {time()-start_time:.2f} seconds to find the last user.")
    else:
        print(f"Error test {test}: couldn't find user u{n}.")
        n_errors += 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.\n")
    else:
        print("WOO HOO, No errors detected.\n")


# **********************************************************
if __name__ == '__main__':
    given_tests()
    user_tests()

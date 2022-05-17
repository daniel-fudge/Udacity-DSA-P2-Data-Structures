#!/usr/bin/env python3

"""Problem 5 of the Data Structures Project.


Notes:

Assumptions:

"""

from __future__ import annotations
from datetime import datetime
import hashlib
from time import time


class Block(object):

    def __init__(self, timestamp: str, data: str, previous_hash: str):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()
        self.next = None

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()


class BlockChain(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data: str):
        timestamp = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
        if self.head is None:
            self.head = Block(timestamp=timestamp, data=data, previous_hash="")
            self.tail = self.head
        else:
            new_block = Block(timestamp=timestamp, data=data, previous_hash=self.tail.hash)
            self.tail.next = new_block
            self.tail = new_block
        self.size += 1

    def get_head(self):
        return self.head

    def __len__(self):
        return self.size

    def __repr__(self):
        if self.size == 0:
            return "Empty BlockChain"
        message = "Timestamp | Data | Hash | Previous Hash (Starting at the head)\n"
        node = self.head
        while node:
            message += " | ".join([node.timestamp, node.data, node.hash, node.previous_hash]) + "\n"
            node = node.next
        return message


# noinspection PyBroadException
def user_tests():
    """Runs the user tests."""

    # Set some testing constants
    n_errors = 0

    # Check the BlockChain print functionality
    print("\nUser test set 1 - print functionality.")
    test = 1
    chain = BlockChain()
    for b in range(5):
        chain.append(data=f"block {b+1}")
    try:
        print(chain)
    except:
        print(f"Error test {test}: Wasn't expecting an exception.")
        n_errors += 1
    else:
        print(f"Test {test} passed, well really have to look hash and previous hash values to verify a pass.")

    # Check the previous hash values
    print("\nUser test set 2 - Check previous hash values.")
    test = 0
    node = chain.get_head()
    for _ in range(4):
        test += 1
        next_node = node.next
        if next_node.previous_hash != node.hash:
            print(f"Error test {test}: Hash values don't match.")
            n_errors += 1
        else:
            print(f"Test {test} passed.")
        node = next_node

    # Check repeated data
    print("\nUser test set 3 - Repeated data.")
    test = 0
    chain = BlockChain()
    for b in range(5):
        chain.append(data=f"Repeated Data")
    node = chain.get_head()
    for _ in range(4):
        test += 1
        next_node = node.next
        if next_node.hash != node.hash:
            print(f"Error test {test}: Hash values don't match.")
            n_errors += 1
        else:
            print(f"Test {test} passed.")
        node = next_node

    # Test invalid arguments
    print("\nUser test set 4 - Invalid arguments.")
    test = 0
    chain = BlockChain()
    for arg in [1, [], {}, None]:
        test += 1
        try:
            # noinspection PyTypeChecker
            chain.append(arg)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # Check the hash values are unique
    print("\nUser test set 5 - Hash uniqueness for a million values, also test large chains and speed.")
    test = 1
    print("Building the million node BlockChain")
    start_time = time()
    chain = BlockChain()
    n = 10**6
    for b in range(n):
        chain.append(data=f"block {b+1}")
    print(f"\tBuilding took {time()-start_time:.2f} seconds.")

    print("Checking all hash values in the chain for uniqueness.")
    start_time = time()
    node = chain.get_head()
    values = [node.hash]
    node = node.next
    while node:
        new_hash = node.hash
        if new_hash in values:
            print(f"Error test {test}: Hash values repeated.")
            n_errors += 1
            break
        node = node.next
    print(f"\tChecking took {time()-start_time:.2f} seconds.")

    test += 1
    if len(chain) == n:
        print("Length of chain also verified")
    else:
        print(f"Error test {test}: expected a length of {n} but got {len(chain)}.")
        n_errors += 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.\n")
    else:
        print("WOO HOO, No errors detected.\n")


# **********************************************************
if __name__ == '__main__':
    user_tests()

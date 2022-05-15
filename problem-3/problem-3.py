#!/usr/bin/env python3

"""Problem 3 of the Data Structures Project.

Notes:
  1. This was tested with Python 3.10.4.

Assumptions:
    1. The encoded data is a string comprised of '0' and '1' characters.
"""

from collections import defaultdict
import sys


class Node(object):
    def __init__(self, value=None, key=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BinaryTree(object):
    def __init__(self):
        self.root = None
        self.map = {}

    def get_root(self) -> Node:
        return self.root

    def set_root(self, node: Node):
        self.root = node

    def make_map(self, node: Node, code: str):

        if node is None:
            return

        # If no left child exists we are at a leaf node
        if node.left is None:
            self.map[node.key] = code
            return

        # If left child exists, update the code a recurse
        self.make_map(node=node.left, code=code + '0')

        # If a right child exists, update the code a recurse
        if node.right is not None:
            self.make_map(node=node.right, code=code + '1')


class MinHeap(object):
    def __init__(self):
        self.array = []
        self.array_size = 0
        self.map = {}

    def extract_root(self) -> Node:
        value = self.array.pop(0)
        self.array_size -= 1
        self.heapify_down(node_number=0)
        return value

    def insert(self, node: Node):
        self.array.append(node)
        self.array_size += 1
        self.heapify_up(node_number=self.array_size-1)

    def get_root(self) -> Node:
        return self.array[0]

    @staticmethod
    def get_parent_index(node_number: int) -> int:
        return (node_number - 1)//2

    @staticmethod
    def get_left_child_index(node_number: int) -> int:
        return node_number * 2 + 1

    @staticmethod
    def get_right_child_index(node_number: int) -> int:
        return node_number * 2 + 2

    def heapify_up(self, node_number: int):
        # Stop if at the root (i=0)
        if node_number > 0:
            parent_index = self.get_parent_index(node_number)
            parent = self.array[parent_index]
            node = self.array[node_number]

            # Swap if larger and recurse up until parent is >= node or at root
            if node.value < parent.value:
                self.array[node_number] = parent
                self.array[parent_index] = node
                self.heapify_up(parent_index)

    def heapify_down(self, node_number: int):

        # Check left first, return if no child exist
        left_child_index = self.get_left_child_index(node_number)
        if left_child_index >= self.array_size:
            return

        node = self.array[node_number]
        left_child = self.array[left_child_index]
        # Swap if left is smaller and recurse until child < node or at the end leaf
        if left_child.value < node.value:
            self.array[node_number] = left_child
            self.array[left_child_index] = node
            self.heapify_down(left_child_index)
        del node, left_child, left_child_index

        # Also make sure the right side is > new parent
        right_child_index = self.get_left_child_index(node_number)
        if right_child_index < self.array_size:
            node = self.array[node_number]
            right_child = self.array[right_child_index]
            # Swap if right is smaller and recurse until child < node or at the end leaf
            if right_child.value < node.value:
                self.array[node_number] = right_child
                self.array[right_child_index] = node
                self.heapify_down(right_child_index)


def make_huffman_tree(frequency: dict) -> BinaryTree:
    huffman_tree = BinaryTree()

    # The priority queue is a Min-Heap
    priority_queue = MinHeap()
    for character, count in frequency.items():
        priority_queue.insert(Node(key=character, value=count))

    # Create the Binary Tree
    #   Note the leaf nodes also contain the key but the composite nodes will have the None default key value
    if len(frequency) == 1:
        huffman_tree.set_root(Node())
    else:
        while priority_queue.array_size > 1:
            # Extract the two lowest frequency nodes from the queue, create a new node with the sum as the value
            node1 = priority_queue.extract_root()
            node2 = priority_queue.extract_root()
            new_value = node1.value + node2.value
            new_node = Node(value=new_value)

            # Add the nodes from the queue as leafs, so they can build up the Huffman Tree
            if node1.key is None and node2.key is not None:
                new_node.left = node1
                new_node.right = node2
            elif node2.key is None and node1.key is not None:
                new_node.left = node2
                new_node.right = node1
            elif node1.value < node2.value:
                new_node.left = node1
                new_node.right = node2
            elif node1.value > node2.value:
                new_node.left = node2
                new_node.right = node1
            elif node1.key is None and node2.key is None:
                new_node.left = node1
                new_node.right = node2
            elif node1.key < node2.key:
                new_node.left = node1
                new_node.right = node2
            else:
                new_node.left = node2
                new_node.right = node1
            huffman_tree.set_root(new_node)

            # Add the subtree to the priority queue as a single node
            priority_queue.insert(node=new_node)

    return huffman_tree


def huffman_encoding(data: str) -> tuple[str, BinaryTree]:
    """The Huffman encoding algorithm.

    Args:
        data (str): The string to encode.

    Returns:
        str: The encoded data.
        BinaryTree: The Huffman binary tree.
    """

    # Return empty objects if the string is empty
    if len(data) == 0:
        return '', BinaryTree()

    # Count the character frequency
    frequency = defaultdict(int)
    for c in data:
        frequency[c] += 1

    # Make the huffman tree and catch the degenerate case of a single unique character
    if len(frequency) == 1:
        huffman_tree = BinaryTree()
        key = [k for k in frequency.keys()][0]
        huffman_tree.set_root(Node(key=key, value=frequency[key]))
    else:
        huffman_tree = make_huffman_tree(frequency)

    # Create the map from character to Huffman Code
    root = huffman_tree.get_root()
    huffman_tree.make_map(node=root, code='')
    mapping = huffman_tree.map

    # Encode the data
    encoded_data = ''.join([mapping[c] for c in data])

    return encoded_data, huffman_tree


def huffman_decoding(data: str, tree: BinaryTree) -> str:
    """Decodes the encoded Huffman data with the associated Tree.

    Args:
        data (str): The string to encode.
        tree (BinaryTree): The Huffman binary tree.

    Returns:
        str: The decoded data.
    """
    decoded_data = ''

    return decoded_data


def given_tests():
    """Runs the given tests."""

    # Set some testing constants
    a_great_sentence = "The bird is the word"

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}\n".format(decoded_data))


def user_tests():
    """Runs the user tests."""

    # Set some testing constants
    n_errors = 0

    # Test the mapping
    print("\nUser test set 1 - Mapping")
    test = 0
    for arg, expected in [("bbccaa", {"b": "00", "c": "01", "a": "1"}), ("rrs", {"r": "1", "s": "0"}), ("t", {"t": ""}),
                          ("AAAAAAABBBCCCCCCCDDEEEEEE", {"A": "10", "B": "001", "C": "11", "D": "000", "E": "01"})]:
        test += 1
        _, huffman_tree = huffman_encoding(arg)
        huffman_tree.make_map(node=huffman_tree.get_root(), code='')
        actual = huffman_tree.map
        success = True
        if len(actual) != len(expected):
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1
            success = False
        else:
            for key in expected.keys():
                if actual[key] != expected[key]:
                    print(f"Error test {test}: for {key} expected {expected[key]} but got {actual[key]}.")
                    n_errors += 1
                    success = False
        if success:
            print(f"Test {test} passed.")

    # Test the encoding
    print("\nUser test set 2 - Encoding")
    test = 0
    for arg, expected in [("AAAAAAABBBCCCCCCCDDEEEEEE", "1010101010101000100100111111111111111000000010101010101"),
                          ("t", ""), ("rrs", "110"), ("bbccaa", "0000010111")]:
        test += 1
        actual, _ = huffman_encoding(arg)
        if actual == expected:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected} but got {actual}.")
            n_errors += 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.\n")
    else:
        print("WOO HOO, No errors detected.\n")


# **********************************************************
if __name__ == '__main__':
    user_tests()
    given_tests()

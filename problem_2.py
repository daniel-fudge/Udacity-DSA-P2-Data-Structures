#!/usr/bin/env python3

"""Problem 2 of the Data Structures Project.

Notes:
    Basically the folder structure is a tree and the task is to traverse the tree and record all files with the given
    suffix. We are traversing it depth first.

Assumptions:
    1. An empty string for the suffix or path is not permitted.
    2. Wild cards are not permitted, i.e. * and other regex
    3. The path must be full and not relative.
    4. If the path doesn't exist, an exception is raised
"""

import os
import shutil
from time import time


def check_folder(folder: str, suffix: str) -> list:
    """Returns a list of files in the given folder that ends in the given suffix.

    Args:
        folder (str): The folder to search.
        suffix (str): the suffix to check.

    Returns:
        list: The files in the given folder ending in the given suffix
    """

    new_files = []
    for path in [os.path.join(folder, f) for f in os.listdir(folder)]:
        if os.path.isfile(path) and path.endswith(suffix):
            new_files.append(path)
        if os.path.isdir(path):
            new_files.extend(check_folder(folder=path, suffix=suffix))

    return new_files


def find_files(suffix: str, path: str) -> list:
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       list: a list of paths

    Raises:
        AttributeError: If the suffix or path are not strings or if an empty string.
    """

    # Check arguments
    for arg, value in [('Suffix', suffix), ('Path', path)]:
        if not isinstance(value, str):
            raise AttributeError(f"{arg} must be a string")
        if len(value) == 0:
            raise AttributeError(f"{arg} can not be an empty string")
    if not os.path.isdir(path):
        raise AttributeError(f"{path} is not a valid folder, note relative paths are not allowed")

    # Get all the paths
    path_list = check_folder(folder=path, suffix=suffix)

    # Remove the base path and switch '\' for '/' (windows)
    unwanted_root = len(os.path.dirname(path)) + 1
    for i, path in enumerate(path_list):
        path_list[i] = "./" + path[unwanted_root:].replace("\\", "/")

    return path_list


def make_folders(path: str, depth: int, max_depth: int, breath: int):
    """Recursive function to create test folder structure.

    Args:
        path (str): The folder to create and make the 'foo.c' file inside of.
        depth (int): The depth of the current path.
        max_depth (int): The max depth to create.
        breath (int): The number of sub folders to create.
    """

    os.mkdir(path)
    with open(os.path.join(path, 'foo.c'), 'w') as f:
        f.write(" ")

    if depth >= max_depth:
        return

    for i in range(breath):
        make_folders(path=os.path.join(path, f"sub{i+1}"), depth=depth+1, max_depth=max_depth, breath=breath)


def run_tests():
    """Runs the user tests."""

    # Set some testing constants
    n_errors = 0
    cwd = os.getcwd()
    test_root = os.path.join(cwd, 'testdir')

    # Add your own test cases: include at least three test cases
    # and two of them must include edge cases, such as null, empty or very large values

    # User test case 1 - nominal operation find '.c'
    print("Test set 1 - Nominal find '.c'")
    expected = ["./testdir/subdir1/a.c",
                "./testdir/subdir3/subsubdir1/b.c",
                "./testdir/subdir5/a.c",
                "./testdir/t1.c"]
    actual = find_files(suffix='.c', path=test_root)
    test = 1
    if len(actual) == len(expected):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected {len(expected)} but got {len(actual)} values.")
        n_errors += 1
    for expected_path in expected:
        test += 1
        if expected_path in actual:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected_path} not in actual {', '.join(actual)} values.")
            n_errors += 1

    # User test case 2 - nominal operation find '.gitkeep'
    print("\nTest set 2 - Nominal find '.gitkeep'")
    test = 1
    expected = ["./testdir/subdir2/.gitkeep",
                "./testdir/subdir4/.gitkeep"]
    actual = find_files(suffix='.gitkeep', path=test_root)
    if len(actual) == len(expected):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected {len(expected)} but got {len(actual)} values.")
        n_errors += 1
    for expected_path in expected:
        test += 1
        if expected_path in actual:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected {expected_path} not in actual {', '.join(actual)} values.")
            n_errors += 1

    # User test case 3 - Nothing found
    print("\nTest set 3 - Nothing found, .foo suffix")
    test = 1
    actual = find_files(suffix='.foo', path=test_root)
    if isinstance(actual, list):
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected an empty list but got a {type(actual)}.")
        n_errors += 1
    test += 1
    if len(actual) == 0:
        print(f"Test {test} passed.")
    else:
        print(f"Error test {test}: expected an empty list but got a {len(actual)} entries.")
        n_errors += 1

    # User test case 4 - Invalid suffix
    print("\nTest set 4 - invalid suffix")
    test = 1
    for suffix in [1, "", [], None]:
        test += 1
        try:
            # noinspection PyTypeChecker
            find_files(suffix=suffix, path=test_root)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User test case 5 - Invalid paths
    print("\nTest set 5 - invalid paths")
    test = 1
    for path in [1, "", "foo", [], None]:
        test += 1
        try:
            # noinspection PyTypeChecker
            find_files(suffix='.c', path=path)
        except AttributeError:
            print(f"Test {test} passed.")
        else:
            print(f"Error test {test}: expected an AttributeError exception.")
            n_errors += 1

    # User test case 6 - Very large folder structure, 10 deep with 3 sub folders = 3^10
    print("\nTest set 5 - Very deep")
    test = 1
    max_depth = 10
    breath = 3
    scratch_folder = os.path.join(cwd, 'scratch')
    if os.path.isdir(scratch_folder):
        print("Deleting old scratch")
        shutil.rmtree(scratch_folder)
    print("Making deep folder structure.")
    make_folders(path=scratch_folder, depth=0, max_depth=max_depth, breath=breath)
    print("Actually running the test.")
    start_time = time()
    actual = find_files(suffix='.c', path=scratch_folder)
    print(f"Executed in {time() - start_time:.3f} seconds.")
    expected_entries = sum([3 ** i for i in range(max_depth + 1)])
    if len(actual) == expected_entries:
        print(f"Test {test} passed, now deleting the scratch folder.")
        shutil.rmtree(scratch_folder)
    else:
        print(f"Error test {test}: expected {expected_entries} entries but got {len(actual)}.")
        n_errors += 1

    print("\n*******************")
    if n_errors > 0:
        raise RuntimeError(f"BOO HOO, {n_errors} errors detected.")
    else:
        print("WOO HOO, No errors detected.")


# **********************************************************
if __name__ == '__main__':
    run_tests()

# Problem 2 of the Data Structures Project
The folder structure we have to search can be thought of as a tree and the task is to traverse the tree and record all 
files with the given suffix. The primary decision is weather to use a depth or breath first search algorithm. Both 
algorithms will have very similar time complexity but the true space complexity will vary depending on the "shape" of 
the tree. If there are many sub-folders in each folder, the size of the search queue for the breath first option would 
become very large. If the folder structure is very deep, the call stack of the depth first algorithm would become very 
large. Unfortunately, we do not know the depth to width ratio for this generic tree, so it is not possible to say which 
will use more memory.   
I've selected the depth first algorithm with recursion for simplicity. A simple loop through all the items in a folder 
saves any matching files to a simple array (list) or recurses down if a folder is found.

### Assumptions:
1. An empty string for the suffix or path is not permitted.
2. Wild cards are not permitted, i.e. * and other regex
3. The path must be full and not relative.
4. If the path doesn't exist, an exception is raised

## Time Efficiency
Since each node (folder) is only visited once the time complexity is O(n), where n is the number of nodes (folders).
However, since we also have to check every file in every folder we have to add O(f) to the time complexity, where f is 
the total number of files (not just the files matching the suffix).    
Therefore, the total time complexity is O(n + f).   
Please see user test 6 where a large folder structure with 10 levels and 3 sub-folders (88,573 nodes) each is searched. 
Although the exact scalability was not determined, we can clearly see that it is not constant nor exponential.    

## Space Efficiency
There are two drivers for the space complexity; the maximum call stack size and the number of files matching the suffix.
In the worst case, each folder would have only one sub-folder making the maximum stack call size = n. For the files, the
worst case would be is all files has the matching suffix.   
Therefore, the worst case space complexity is also O(n + f). In practice, I suspect the space complexity would be much 
less.

# Problem 4 of the Data Structures Project
This code searches for a user in a group/user hierarchy and returns True if found and False otherwise.    
The group/user hierarchy is effectively a tree structure where each group is a node and the users are the values in each
node.  Therefore, this is a tree search task.    
The primary decision is weather to use a depth or breath first search algorithm. Both algorithms will have very similar 
time complexity but the true space complexity will vary depending on the "shape" of the tree. If there are many 
subgroups in each group, the size of the search queue for the breath first option would become very large. If the group 
structure is very deep, the call stack of the depth first algorithm would become very large. Unfortunately, we do not 
know the depth to width ratio for this generic tree, so it is not possible to say which will use more memory.   
I've selected the Breath First Search (BFS) with a simple while loop that continues until the user is found or the 
search queue is empty, meaning the user is not found.    
For the search queue, I'll use a simple list. Nothing more complicated is required since we only need to add and pull 
items from the two ends of the list.

### Assumptions
1. Duplicate user and group names are acceptable.

## Time Efficiency
Since each node (group) is only visited once in the worst case, the time complexity is O(n), where n is the number of 
nodes. However, since we also have to check every user in every group in the worst case, we have to add O(u) to the time 
complexity, where u is the total number of users. Therefore, the total time complexity is O(n + u).     
Note if the user is found, both the time and complexity will be much lower.  
Please see user test 4 where a large structure with 1 million groups and users (1 user per group) is searched for the 
last user (close to worst case). 
Although the exact scalability was not determined, we can clearly see that it is not constant nor exponential.    

## Space Efficiency
The space complexity of the group itself is simply the number of groups (n) plus the number of users (u) or O(n + u). 
Note some groups may have no users, so contain an empty list. This has a minimal impact on the overall space complexity, 
and it remains O(n+u).
Since we don't have to save a new list of users, but simply exit when the user is found, the search space complexity is 
dependent on the maximum search queue size. The worst case would be if all n-1 subgroups are within the top group.    
Therefore, the worst case space complexity is also O(n - 1) = O(n). In practice, I suspect the space complexity would be 
much as groups would be nested.

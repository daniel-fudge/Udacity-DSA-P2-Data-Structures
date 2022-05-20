# Problem 6 of the Data Structures Project
This problem creates functions to find the union and intersection of two given singly linked lists. This code could have 
been simplified by using the builtin Python set Type union and intersection operations. They weren't used to 
illustrate the basic functionality.   
How to handle duplicates and the resulting order wasn't defined, it was assumed that duplicates would be ignored and the 
resulting order of the list will be based on the first list and then the second.       
Both the union and intersection function were made very simplistic by adding a `get_unique_values` method to the linked 
list. This method simply traverses the list and builds a set of unique values. With a set of the unique values of each 
list, simple list comprehension can generate the desired union and intersection.   
A set was used instead of a list to greatly reduced the time complexity of the membership test within each of the list 
comprehensions. If it was a simple list, a single check would have to traverse the full list in the worst case. 
Python's `set` data structure is a hash table so the average membership check is O(1) instead of O(n) for lists. 

### Assumptions
1. Duplicates in the input lists are ignored, therefore no duplicates in the union and intersection output.
2. Order of the linked lists does not need to be maintained.

## Time Efficiency
Building the unique sets requires a pass through all the elements of the list and a membership check. Since we are using 
a set (hashtable), the membership check is constant so building two sets is O(n + m), where n and m are the number of 
nodes in the first and second linked lists.   
With the two sets, the intersection only requires a pass though all elements of the first list to add a node to the new 
linked list if the membership in the second list is true.  Therefore, the time complexity of the intersection is 
O(n + m) + O(n) = O(n + m). Since the intersection is only dependent on the first list, we should make the "first" list
the smaller of the two lists.   
The union requires a pass through the first list to add all the values to the new list and then a pass through the 
second list and only adding the values to the new list if the second value is also a member of the first list.  
Therefore, the union time complexity is O(m + n) + O(m + n) = O(m + n).   
Please note the last user test that compares the intersection and union times from a pair of 1 million node lists with a 
pair of 10,000 node lists. As expected, the union is always longer than the intersection by about 3 times (constant). 
We also see that increasing m and n by 100 times increases the run times by 100-200 times. The exact ratio varies each 
time the test runs due to the random selection of the list values. However, both the union and intersection times agree
with the O(m + n) analysis.

## Space Efficiency
The worst case space complexity would occur if both list didn't contain duplicates. Therefore, the new sets would have a 
O(n + m) space complexity.
The union worst case would occur if there were no duplicates between the two lists resulting in O(m + n).  Adding the 
unique sets gives O(m + n) + O(m + n) = O(m + n).
The intersection worst case occurs when the two sets are the same, resulting in O(min(n + m)). Adding the unique sets 
gives O(m + n) + O(min(n + m)) = O(n + m).



# Problem 1 of the Data Structures Project
This problem implements the Least Recently Used (LRU) Cache with a doubly linked list plus a map. 
Adding the map to the linked list doubles the space complexity but makes the time efficiency for get operations 
constant. Without the map, in the worst case we would have to traverse the full linked list to find the node being 
accessed. 
The linked list is required to keep track of the order in which the nodes have been accessed. A simple queue or stack
could not be used because we need to access node from anywhere in stack, not just from the ends. We need a doubly linked
instead of a singly linked list, because the map points directly to a node. To then remove and place at the head of the 
linked list we need to know the previous node as well as the next node. If we only knew the next node, we would again 
have to in the worst case traverse the full linked list to find the previous node.  

## Assumptions
1. Both the key and value of the cache must be integers.
2. 'Use' is defined as both 'set' and 'get' access, e.i. both methods place the node at the head of the Cache. 
3. The most recently used node is placed at the head of the Doubly Linked List (Cache).
4. A capacity less than 2 is not valid, as it would be degenerate.

## Time Efficiency
As discussed above, the combination of a map and doubly linked list make the time efficiency constant O(1) for both set 
and get operations for this implementation.
Please notice user test case 5.7, which verifies the constant time complexity upto a linked list of 1 million nodes.

## Space Efficiency
As for any cache, we have to save the data for every node in the cache which makes the space efficiency O(n), when n is 
the number of nodes. Each node must save the key, value and pointers to point the next and previous node (4 items). In 
this example the values are simple integers, so are the same magnitude as the other items giving O(4n).
The actual cache object also stores the capacity, number of elements and points to both the head and tail of the linked 
list, which are independent of n, so a constant 4 items. This implementation also stores a map which contains a key and 
pointer to every node in the list, which makes it O(2n+4) in space complexity.
Adding both the linked list and cache with the map gives a space efficiency of O(6n+4) or simplified to O(n). 

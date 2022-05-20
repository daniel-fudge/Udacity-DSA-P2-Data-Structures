# Problem 5 of the Data Structures Project
This problem is a simple BlockChain implementation using a singly linked list. Since there is no requirement (by design)
to append a node (Block) anywhere expect the tail of the linked list (BlockChain) we have no need of a node hash map or 
a doubly linked list.  
The only feature that makes the BlockChain different from a regular singly linked list is the creation time stamp and 
hash of the data on each node plus the hash of the previous node. By saving the previous hash, we can detect if the data 
within the previous node was altered.

## Time Efficiency
Since we only append nodes to the tail of the list, the "append" time complexity is constant = O(1). Getting the head is
also constant. The operations that aren't constant is the print (`__repr__`) and if you wanted to find a specific node. 
Both of these would have to traverse the full list in the worst case so are O(n), where n is the total number of nodes.  

## Space Efficiency
Each node in the list contains five elements. The size of the data and hashes may be large so the actual memory used is 
not known but the space complexity will still only scale with the number of nodes.  Therefore, the space complexity is 
O(n). 

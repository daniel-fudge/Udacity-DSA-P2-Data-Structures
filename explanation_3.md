# Problem 3 of the Data Structures Project
This problem consists of two different data structures and the logic to encode and decode the data. As the rubric says 
not to walk through the code, I'll let the code speak to the encoding and decoding logic as it's fairly 
self-explanatory.   
The Huffman Tree itself is a standard binary tree consisting of nodes with a key value and left and right children. 
Building the tree follows the given logic, which pulls two items from a priority queue and adds the resulting value sum 
as a new node until the priority queue is finished.    
This leads to the second data structure, which is the most interesting. The above loop is constantly adding items to the 
priority queue, which wouldn't be an issue if the items were always added an end of the queue, but the item must be 
inserted within the queue based on the frequency sums. If we used a simple list, we would have to traverse the full list
in the worst case for every addition to the priority queue.  Because of this requirement, a binary min-heap was selected 
for the priority queue.  This makes the insertion in the worst case O(log n), where n in the number of nodes, which is 
better than O(n). For a random heap with multiple insertions, the time complexity drops to O(1) [Mehlhorn, 1989](https://publikationen.sulb.uni-saarland.de/handle/20.500.11880/26179).    
The min-heap itself is simply an array. However, because it represents a complete binary tree we can explicitly define 
the index of the parent (i-1//2) and both the left (2i+1) and right (2i+2) child of every node i.  When adding nodes to 
the min-heap, we first add the node to the last open position which is just at the end of the array and then recursively 
switch the parent with the new node if the parent is smaller. We also have to recurse down if the new parent is smaller 
than the other child. 

### Assumptions:
1. The encoded data is a string comprised of '0' and '1' characters.

## Time Efficiency
### Encoding the data
The first step in building the tree is calculating the frequencies, which is simply O(n) where n is the number of total 
characters in the given string.    
The next step is creating the initial priority queue. This requires adding the m unique characters to a growing 
min-heap. At the start the min-heap is empty so the insert is clearly constant. The last (worst-case) character is 
inserted into a min-heap of size (m-1).  As mentioned above, the worst case insertion here is O{log(m-1)} but on 
average for random heap is O(1). Therefore, the total time complexity would be worst case O{m log(m-1)} = O(m log m).   
Once the initial queue is generated, we have to build the Huffman binary tree, which consists of removing two nodes and 
then adding one until the queue is exhausted. Note you don't have to add to the queue after removing the last two so 
there are m-2 insertions.  Actually creating the Huffman tree is O(1) since it is simply combining two heads into a new 
node. Therefore, the time complexity is worst case O{(m-2) * log m} = O(m log m).   
The same logic hold for the deletion of nodes, which gives another O(m log m).    
With the tree created, we have to encode each of the n characters, which requires traversing the full depth of the tree.
The worst case depth of the tree would be m-1 so the time complexity would be O{n(m-1)} = O(nm).
Adding these three together we get worst case O(n + nm + m log m).
Additionally, we know m is limited in size since it is the number of unique characters. Assuming 8-bit ASCII characters,
this is 256. If the string was much larger than this, we can further simplify the time complexity to O(n).

### Decoding the data
Decoding is simply the time to traverse the tree, which is the Huffman tree height. Worst case this is m-1 so the time 
complexity is O{n(m-1)}. Making the same assumption as above where n >>> m, this further simplifies to O(n).  

## Space Efficiency
### Encoding the data
To start we clearly need to store the initial string of n characters, so we at least need n bytes of memory. The 
size of the frequency and initial priority queue is the number of unique characters m, so we have O(n + m).    
As we build the Huffman tree, the min-heap shrinks so we no longer have to consider it as it is captured above.    
Since the Huffman tree is a binary tree, the total number of total nodes will not be double the m leaf nodes.  
Therefore, the space complexity is O(m).   
Adding all the components together we get O(n + m), which again assuming n >>> m, gives O(n).

### Decoding the data
When decoding with the huffman tree the number of characters to decode p does not have to equal the original number of 
characters n but are limited to the set of m characters.  Since we are using the Huffman tree with space complexity 
O(m) we get a total space complexity of O(p + m). Again if we assume p >>> m, this simplifies to O(p).    


"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from copy import deepcopy
from random import randint, shuffle
from time import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_repr = ""
            if node != None:
                str_repr += recurse(node.right, level + 1)
                str_repr += "| " * level
                str_repr += str(node.data) + "\n"
                str_repr += recurse(node.left, level + 1)
            return str_repr

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return: int
            '''
            if top is None:
                return -1
            else:
                return 1 + max([height1(top.left), height1(top.right)])

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() < 2 * log(self._size + 1, 2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''Returns a list of the items in the
        tree, where low <= item <= high.'''

        result = []
        for element in self:
            if low <= element <= high:
                result.append(element)
        return result

    def rebalance(self):
        '''Rebalances the tree.'''

        el_list = []
        for element in self:
            el_list.append(element)
        self.clear()

        def add_el_from_midle(el_list):
            el_list = sorted(el_list)
            try:
                middle = el_list[len(el_list)//2]
                self.add(middle)
                add_el_from_midle(el_list[:len(el_list)//2])
                add_el_from_midle(el_list[1+len(el_list)//2:])
            except IndexError:
                pass

        add_el_from_midle(el_list)
        return self

    def successor(self, item):
        """Returns the smallest item that is larger than
        item, or None if there is no such item."""

        prev = None
        for element in self.inorder():
            print('prev:', prev, 'elem:', element)
            if prev == item:
                return element
            elif element > item:
                return element
            prev = element

    def predecessor(self, item):
        """Returns the largest item that is smaller than
        item, or None if there is no such item."""

        prev = None
        for element in self.inorder():
            if element == item or element > item:
                return prev
            prev = element

    def demo_bst(self, path):
        """Demonstration of efficiency binary
        search tree for the search tasks."""
    
        with open(path, mode='r', encoding='utf-8') as words_file:
            original_words_list = words_file.read().split('\n')

        #Creating a list of 10000 random words.
        temp_list = deepcopy(original_words_list)
        list_of_random_words = []
        for _ in range(10000):
            index = randint(0, len(temp_list)-1)
            list_of_random_words.append(temp_list[index])
            del temp_list[index]

        #In order to avoid recursion error we should change the size of original list
        original_words_list = original_words_list[:900]

        #search using methods of the built-in type list.
        print('Search using methods of the built-in type list')
        start_time = time()
        for word in list_of_random_words:
            result = word in original_words_list
        print('{} seconds\n'.format(time()-start_time))

        #Сreating a binary search tree by adding words to the tree
        #from a dictionary that is sorted alphabetically.
        linked_bst_case1 = LinkedBST()
        for word in original_words_list:
            linked_bst_case1.add(word)

        #search for words in a binary tree, words in which were added in alphabetical order.
        print('Search for words in a binary tree, words in which were added in alphabetical order')
        start_time = time()
        for word in list_of_random_words:
            result = word in linked_bst_case1
        print('{} seconds\n'.format(time()-start_time))
        
        #Сreating a binary search tree by adding words to the tree
        #from a dictionary that is arranged in random order.
        shuffled_list = deepcopy(original_words_list)
        shuffle(shuffled_list)
        linked_bst_case2 = LinkedBST()
        for word in shuffled_list:
            linked_bst_case2.add(word)

        #search for words in a binary tree, words in which were added in random order.
        print('Search for words in a binary tree, words in which were added in random order')
        start_time = time()
        for word in list_of_random_words:
            result = word in linked_bst_case2
        print('{} seconds\n'.format(time()-start_time))
        
        #search for words in a balanced binary tree.
        linked_bst_case1.rebalance()
        print('Search for words in a balanced binary tree')
        start_time = time()
        for word in list_of_random_words:
            result = word in linked_bst_case1
        print('{} seconds\n'.format(time()-start_time))

if __name__ == '__main__':
    tree = LinkedBST()
    tree.demo_bst('words.txt')

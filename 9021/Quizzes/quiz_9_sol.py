# Generates a binary tree T whose shape is random and whose nodes store
# random even positive integers, both random processes being directed by user input.
# With M being the maximum sum of the nodes along one of T's branches, minimally expands T
# to a tree T* such that:
# - every inner node in T* has two children, and
# - the sum of the nodes along all of T*'s branches is equal to M.
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, randrange

from binary_tree_adt import *


def create_tree(tree, for_growth, bound):
    if randrange(max(for_growth, 1)):
        tree.value = 2 * randrange(bound + 1)
        tree.left_node = BinaryTree()
        tree.right_node = BinaryTree()
        create_tree(tree.left_node, for_growth - 1, bound)
        create_tree(tree.right_node, for_growth - 1, bound)


def expand_tree(tree):
    if tree.value is not None:
        _expand_tree(tree, max_branch_sum(tree))
    
def max_branch_sum(tree):
    if tree.value is None:
        return 0
    return tree.value + max(max_branch_sum(tree.left_node), max_branch_sum(tree.right_node))

def _expand_tree(tree, target):
    target -= tree.value
    if not target:
        return
    if tree.left_node.value is None:
        tree.left_node = BinaryTree(target)
    if tree.right_node.value is None:
        tree.right_node = BinaryTree(target)
    if tree.left_node.value is not None:
        _expand_tree(tree.left_node, target)
    if tree.right_node.value is not None:
        _expand_tree(tree.right_node, target)

                
try:
    for_seed, for_growth, bound = [int(x) for x in input('Enter three positive integers: ').split()
                                   ]
    if for_seed < 0 or for_growth < 0 or bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
 
seed(for_seed)
tree = BinaryTree()
create_tree(tree, for_growth, bound)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
expand_tree(tree)
print('Here is the expanded tree:')
tree.print_binary_tree()




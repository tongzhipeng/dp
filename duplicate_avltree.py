#original source from https://github.com/pgrafov/python-avl-tree
#support insert same key to the tree
#to do!!! code rearrange
import random, math

from pyavltree import Node
from pyavltree import AVLTree
from pyavltree import random_data_generator


class DuplicateNode(Node):
    def __init__(self, key):
        self.count = 1
        super(DuplicateNode, self).__init__(key)


class DuplicateAVLTree(AVLTree):
    def __init__(self, *args):     
        super(DuplicateAVLTree, self).__init__(*args)


    def insert(self, key):
        new_node = DuplicateNode(key)
        if not self.rootNode:
            self.rootNode = new_node
        else:
            node = self.find(key)
            if node is None:
                self.elements_count += 1
                self.add_as_child(self.rootNode, new_node)
            else:
                node.count += 1

    def inorder_non_recursive(self):
        node = self.rootNode
        retlst = []
        while node.leftChild:
            node = node.leftChild
        while (node):
            retlst += [node.key] * node.count
            if (node.rightChild):
                node = node.rightChild
                while node.leftChild:
                    node = node.leftChild
            else:
                while ((node.parent) and (node == node.parent.rightChild)):
                    node = node.parent
                node = node.parent
        return retlst

    def preorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        retlst += [node.key] * node.count
        if node.leftChild:
            retlst = self.preorder(node.leftChild, retlst)
        if node.rightChild:
            retlst = self.preorder(node.rightChild, retlst)
        return retlst

    def inorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.leftChild:
            retlst = self.inorder(node.leftChild, retlst)
        retlst += [node.key] * node.count
        if node.rightChild:
            retlst = self.inorder(node.rightChild, retlst)
        return retlst

    def postorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.leftChild:
            retlst = self.postorder(node.leftChild, retlst)
        if node.rightChild:
            retlst = self.postorder(node.rightChild, retlst)
        retlst += [node.key] * node.count
        return retlst


    def get_pre_sub_tree(self, node, key_max_value):
        if node is None:
            return None
        pre_tree_node = node
        min_left_parent_value = None
        min_left_parent = None
        while pre_tree_node and pre_tree_node.key > key_max_value:
            if pre_tree_node.parent:
                if pre_tree_node.parent.rightChild == pre_tree_node:
                    if min_left_parent_value is None or min_left_parent_value > pre_tree_node.parent.key:
                        min_left_parent_value = pre_tree_node.parent.key
                        min_left_parent = pre_tree_node.parent
                pre_tree_node = pre_tree_node.parent
            else:
                break

        if pre_tree_node.key <= key_max_value:
            return pre_tree_node
        elif min_left_parent is None:
            return node.leftChild
        return min_left_parent

    def get_pre_node(self, node):
        if node.leftChild:
            prev_node = node.leftChild
            while prev_node.rightChild:
                prev_node = prev_node.rightChild
        elif node.parent and node.parent.rightChild == node:
            prev_node = node.parent
        else:
            prev_node = node.parent
            cur = node
            while prev_node and prev_node.leftChild == cur:
                cur = prev_node
                prev_node = prev_node.parent
        return prev_node


    def remove_node(self, node):
        if node is not None and node.count > 1:
            node.count -= 1
            return
        super(DuplicateAVLTree, self).remove_node(node)


    def remove_leaf(self, node):
        assert node.count == 1
        super(DuplicateAVLTree, self).remove_leaf(node)

    def remove_branch(self, node):
        assert node.count == 1
        super(DuplicateAVLTree, self).remove_branch(node)


if __name__ == "__main__":
    """check empty tree creation"""
    a = DuplicateAVLTree()
    a.sanity_check()

    """duplicate elments"""
    duplicate_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 3
    seq_copy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 3
    duplicate_seq.sort()
    seq_copy.sort()
    # random.shuffle(seq)
    b = DuplicateAVLTree(duplicate_seq)
    b.sanity_check()

    """check that inorder traversal on an AVL tree 
    (and on a binary search tree in the whole) 
    will return values from the underlying set in order"""
    l1 = b.as_list(3)
    l2 = b.as_list(1)
    assert (b.as_list(3) == b.as_list(1) == seq_copy)

    """check that node deletion works"""
    c = DuplicateAVLTree(random_data_generator(10000))
    before_deletion = c.elements_count
    for i in random_data_generator(1000):
        c.remove(i)
    after_deletion = c.elements_count
    c.sanity_check()
    assert (before_deletion >= after_deletion)
    # print c.out()

    """check that an AVL tree's height is strictly less than 
    1.44*log2(N+2)-1 (there N is number of elements)"""
    assert (c.height() < 1.44 * math.log(after_deletion + 2, 2) - 1)
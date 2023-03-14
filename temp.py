def quick_sort(arr):
    """This function takes an array as input and sorts it using Quick Sort algorithm."""
    if len(arr) <= 1:
        return arr

    pivot = arr[0] 
    left = []
    right = []

    for i in range(1, len(arr)):
        if arr[i] < pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])

    # Recursively sort the left and right sub-arrays
    left_sorted = quick_sort(left)
    right_sorted = quick_sort(right)

    # Combine the sorted sub-arrays with the pivot element
    return left_sorted + [pivot] + right_sorted

# 给出基于python的二叉树中序遍历代码

class Node:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

def inorderTraversal(root: Node):
    res = []
    if not root:
        return res
    stack = []
    while True:
        if root:
            stack.append(root)
            root = root.left
        elif stack:
            node = stack.pop()
            res.append(node.val)
            root = node.right
        else:
            break
    return res


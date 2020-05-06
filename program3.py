class Node:
    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None

def print_LevelOrder(root):
    if root is None:
        return
    queue = []
    queue.append(root)
    l=[]
    while (len(queue) > 0):
        l.append(queue[0].data)
        node = queue.pop(0)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return ("->".join([str(i)for i in l]))
root = Node(1)
root.right = Node(2)
root.right.right = Node(5)
root.right.right.left = Node(3)
root.right.right.right = Node(6)
root.right.right.left.right = Node(4)
print(print_LevelOrder(root))
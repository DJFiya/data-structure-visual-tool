class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def build_binary_tree(values):
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        current = queue.pop(0)
        if current:
            if i < len(values):
                left_val = values[i]
                current.left = TreeNode(left_val) if left_val is not None else None
                queue.append(current.left)
                i += 1
            if i < len(values):
                right_val = values[i]
                current.right = TreeNode(right_val) if right_val is not None else None
                queue.append(current.right)
                i += 1

    return root
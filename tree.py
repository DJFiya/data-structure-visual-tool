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

class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

def build_avl_tree(values):
    def insert(root, key):
        if not root:
            return AVLNode(key)
        elif key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)

        root.height = 1 + max(get_height(root.left), get_height(root.right))

        balance = get_balance(root)

        # Left Heavy
        if balance > 1 and key < root.left.val:
            return right_rotate(root)
        # Right Heavy
        if balance < -1 and key > root.right.val:
            return left_rotate(root)
        # Left-Right
        if balance > 1 and key > root.left.val:
            root.left = left_rotate(root.left)
            return right_rotate(root)
        # Right-Left
        if balance < -1 and key < root.right.val:
            root.right = right_rotate(root.right)
            return left_rotate(root)

        return root

    def get_height(node):
        return node.height if node else 0

    def get_balance(node):
        return get_height(node.left) - get_height(node.right) if node else 0

    def left_rotate(z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))

        return y

    def right_rotate(z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))

        return y

    root = None
    for val in values:
        if val is not None:
            root = insert(root, val)
    return root
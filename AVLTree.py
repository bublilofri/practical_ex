# AVLTree.py
# username - ofribooblil
# id1      - 325118891
# name1    - ofri booblil
# id2      - 214203747
# name2    - roni bitan
class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def is_real_node(self):
        return self.key is not None

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def _update_height_node(self):
        self.height = 1 + max(self.left.height, self.right.height)

    def rotate_L(self):
        y = self.right
        self.right = y.left
        if y.left.is_real_node():
            y.left.parent = self
        y.parent = self.parent
        y.left = self
        self.parent = y
        self._update_height_node()
        y._update_height_node()
        return y

    def rotate_R(self):
        y = self.left
        self.left = y.right
        if y.right.is_real_node():
            y.right.parent = self
        y.parent = self.parent
        y.right = self
        self.parent = y
        self._update_height_node()
        y._update_height_node()
        return y

    def rotate_LR(self):
        self.left = self.left.rotate_L()
        self.left.parent = self
        return self.rotate_R()

    def rotate_RL(self):
        self.right = self.right.rotate_R()
        self.right.parent = self
        return self.rotate_L()


class AVLTree:
    def __init__(self):
        self.virtual = AVLNode(None, None)
        self.virtual.left = self.virtual.right = self.virtual.parent = self.virtual
        self.virtual.height = -1

        self.root = self.virtual
        self.max_node = self.virtual
        self._size = 0
        self._bf0_count = 0

        self._inorder_cache = []
        self._cache_valid = False

        # for simple tests expecting attribute access
        self.get_root = None

    def get_root(self):
        return None if not self.root.is_real_node() else self.root

    def size(self):
        return self._size

    def get_size(self):
        return self._size

    def search(self, key):
        node = self.root
        while node.is_real_node():
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def _update_height(self, node):
        node.height = 1 + max(node.left.height, node.right.height)

    def _balance_factor(self, node):
        return node.left.height - node.right.height

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        if y.left.is_real_node():
            y.left.parent = z
        y.parent = z.parent

        if z.parent == self.virtual:
            self.root = y
        elif z == z.parent.left:
            z.parent.left = y
        else:
            z.parent.right = y

        y.left = z
        z.parent = y

        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        if y.right.is_real_node():
            y.right.parent = z
        y.parent = z.parent

        if z.parent == self.virtual:
            self.root = y
        elif z == z.parent.right:
            z.parent.right = y
        else:
            z.parent.left = y

        y.right = z
        z.parent = y

        self._update_height(z)
        self._update_height(y)
        return y

    def _rebalance_with_count(self, node):
        count = 0
        while node != self.virtual:
            old_bf = self._balance_factor(node)
            old_height = node.height

            self._update_height(node)
            new_bf = self._balance_factor(node)

            if old_bf == 0 and new_bf != 0:
                self._bf0_count -= 1
            elif old_bf != 0 and new_bf == 0:
                self._bf0_count += 1

            if new_bf > 1:
                if self._balance_factor(node.left) < 0:
                    # LR
                    self._rotate_left(node.left); count += 1
                    self._rotate_right(node);     count += 1
                else:
                    # LL
                    self._rotate_right(node);     count += 1
            elif new_bf < -1:
                if self._balance_factor(node.right) > 0:
                    # RL
                    self._rotate_right(node.right); count += 1
                    self._rotate_left(node);        count += 1
                else:
                    # RR
                    self._rotate_left(node);       count += 1
            elif node.height != old_height:
                count += 1 
            else:
                break
            node = node.parent
        return count

    def insert(self, key, val, start="root"):
        """
        Insert key,val or overwrite existing.
        Returns rotation count.
        """
        self._cache_valid = False

        # if empty tree
        if not self.root.is_real_node():
            z = AVLNode(key, val)
            z.left = z.right = self.virtual
            z.parent = self.virtual
            self.root = z
            self.max_node = z
            self._size = 1
            self.get_root = self.root
            self._bf0_count = 1
            return 0

        # pick start
        current = self.max_node if start == "max" and self.max_node.is_real_node() else self.root

        # walk BST, check duplicates
        parent = self.virtual
        node = current
        while node.is_real_node():
            parent = node
            if key == node.key:
                node.value = val
                self.get_root = self.root
                return 0
            node = node.left if key < node.key else node.right

        # insert new node
        z = AVLNode(key, val)
        z.left = z.right = self.virtual
        z.parent = parent
        if key < parent.key:
            parent.left = z
        else:
            parent.right = z
        
        self._bf0_count += 1    
        self._size += 1
        if key > self.max_node.key:
            self.max_node = z

        ops = self._rebalance_with_count(parent)
        self.get_root = self.root
        return ops

    def delete(self, node):
        if node is None or not node.is_real_node():
            return 0
        self._cache_valid = False

        if not node.left.is_real_node() or not node.right.is_real_node():
            y = node
        else:
            y = node.right
            while y.left.is_real_node():
                y = y.left

        x = y.left if y.left.is_real_node() else y.right
        x.parent = y.parent

        if y.parent == self.virtual:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        if y != node:
            node.key = y.key
            node.value = y.value
        
        old_bf = self._balance_factor(y)
        if old_bf == 0:
            self._bf0_count -= 1

        self._size -= 1
        if node == self.max_node:
            if self._size == 0:
                self.max_node = self.virtual
            else:
                m = self.root
                while m.right.is_real_node():
                    m = m.right
                self.max_node = m

        ops = self._rebalance_with_count(x.parent)
        self.get_root = self.root if self.root.is_real_node() else None
        return ops

    def avl_to_array(self):
        """
        In-order list of (key,value).
        Best: O(1) cache; Worst: O(n); Amortized: O(1) after first
        """
        if self._cache_valid:
            return self._inorder_cache
        res = []
        def inorder(n):
            if not n.is_real_node():
                return
            inorder(n.left)
            res.append((n.key, n.value))
            inorder(n.right)
        inorder(self.root)
        self._inorder_cache = res
        self._cache_valid = True
        return res

    def get_predecessor(self, node):
        """
        Largest key < node.key, or None.
        Best: O(1); Worst: O(log n)
        """
        if node.left.is_real_node():
            n = node.left
            while n.right.is_real_node():
                n = n.right
            return n
        y = node.parent
        while y != self.virtual and node == y.left:
            node, y = y, y.parent
        return None if y == self.virtual else y

    def get_successor(self, node):
        """
        Smallest key > node.key, or None.
        Best: O(1); Worst: O(log n)
        """
        if node.right.is_real_node():
            n = node.right
            while n.left.is_real_node():
                n = n.left
            return n
        y = node.parent
        while y != self.virtual and node == y.right:
            node, y = y, y.parent
        return None if y == self.virtual else y

    # def get_amir_balance_factor(self):
    #     """
    #     Fraction of nodes with balance factor 0.
    #     Time: Θ(n) each call.
    #     """
    #     if self._size == 0:
    #         return 0.0
    #     count0 = 0
    #     def dfs(n):
    #         nonlocal count0
    #         if not n.is_real_node():
    #             return
    #         if self._balance_factor(n) == 0:
    #             count0 += 1
    #         dfs(n.left)
    #         dfs(n.right)
    #     dfs(self.root)
    #     return count0 / self._size
    def get_amir_balance_factor(self):
        if self._size == 0:
            return 0.0
        return self._bf0_count / self._size
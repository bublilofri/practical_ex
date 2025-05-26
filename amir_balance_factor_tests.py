
# -------------------------- UNIT TESTS FOR AMIR BALANCE FACTOR --------------------------
import unittest
import random
import sys
from AVLTree import AVLTree

sys.setrecursionlimit(20000)



def naive_get_amir_balance_factor(tree):
    if tree.root is None or not tree.root.is_real_node():
        return 0
    stack = [tree.root]
    zero = 0
    while stack:
        node = stack.pop()
        if not node.is_real_node():
            continue
        bf = tree._balance_factor(node)
        if bf == 0:
            zero += 1
        stack.append(node.left)
        stack.append(node.right)
    return zero / tree._size


class TestAmirBalanceFactor(unittest.TestCase):
    """Extensive tests ensuring `try_get_amir_balance_factor` stays correct
    and in sync with the O(n) reference implementation `get_amir_balance_factor`
    under a wide range of tree states and operations.
    """

    # ---------- helper -------------------------------------------------
    def _assert_ratio_consistency(self, tree: "AVLTree"):
        """Verify the fast O(1) method matches the reference O(n) scan."""
        self.assertAlmostEqual(
            naive_get_amir_balance_factor(tree),
            tree.get_amir_balance_factor(),
            places=10,
            msg="Mismatch between O(1) and O(n) balance‑factor computations.",
        )

    # ---------- basic states -------------------------------------------
    def test_empty_tree(self):
        tree = AVLTree()
        self.assertEqual(tree.get_amir_balance_factor(), 0)
        self._assert_ratio_consistency(tree)

    def test_single_node(self):
        tree = AVLTree()
        tree.insert(42, "root")
        self._assert_ratio_consistency(tree)
        self.assertEqual(tree.get_amir_balance_factor(), 1)

    # ---------- deterministic insertion patterns -----------------------
    def test_increasing_inserts(self):
        tree = AVLTree()
        for key in range(1, 101):  # triggers repeated RR rotations
            tree.insert(key, str(key))
            self._assert_ratio_consistency(tree)

    def test_decreasing_inserts(self):
        tree = AVLTree()
        for key in range(100, 0, -1):  # triggers repeated LL rotations
            tree.insert(key, str(key))
            self._assert_ratio_consistency(tree)

    def test_insert_with_start_max(self):
        tree = AVLTree()
        for key in range(1, 101):
            tree.insert(key, str(key), start="max")
            self._assert_ratio_consistency(tree)

    # ---------- mixed rotations & structural changes -------------------
    def test_specific_rotation_patterns(self):
        tree = AVLTree()
        # Sequence crafted to cause LL, RR, LR and RL rotations
        sequence = [10, 20, 30, 25, 5, 15, 27, 19, 16, 18]
        for key in sequence:
            tree.insert(key, str(key))
            self._assert_ratio_consistency(tree)

        # Now delete some nodes to trigger re‑balances on removal
        for key in [25, 27, 20, 10]:
            node = tree.search(key)
            tree.delete(node)
            self._assert_ratio_consistency(tree)

    # ---------- randomised smoke testing -------------------------------
    def test_random_inserts_and_deletes(self):
        """Stress‑test with many random sequences to cover edge‑cases."""
        for seed in range(10):  # ten independent runs for determinism
            random.seed(seed)
            keys = random.sample(range(1_000), 200)

            tree = AVLTree()
            # inserts
            for key in keys:
                tree.insert(key, str(key))
                self._assert_ratio_consistency(tree)

            # deletes (half of them)
            random.shuffle(keys)
            for key in keys[:100]:
                node = tree.search(key)
                tree.delete(node)
                self._assert_ratio_consistency(tree)

    # ---------- deletion to exhaustion ---------------------------------
    def test_delete_to_empty(self):
        tree = AVLTree()
        for key in (50, 20, 70):
            tree.insert(key, str(key))
        self._assert_ratio_consistency(tree)
        self.assertEqual(tree.get_amir_balance_factor(), 1)
        for key in (50, 20, 70):
            node = tree.search(key)
            tree.delete(node)
            self._assert_ratio_consistency(tree)

        self.assertEqual(tree.get_amir_balance_factor(), 0)


    # ---------- extreme key values -------------------------------------
    def test_extreme_key_values(self):
        tree = AVLTree()
        extremes = [-2**31, -10**9, -1, 0, 1, 10**9, 2**31 - 1]
        for k in extremes:
            tree.insert(k, str(k))
            self._assert_ratio_consistency(tree)

        random.shuffle(extremes)
        for k in extremes:
            node = tree.search(k)
            tree.delete(node)
            self._assert_ratio_consistency(tree)

        self.assertEqual(tree.get_amir_balance_factor(), 0)

    # ---------- repeated insert‑delete of same key ----------------------
    def test_repeated_insert_delete_same_key(self):
        tree = AVLTree()
        for _ in range(100):
            tree.insert(123, "v")
            self._assert_ratio_consistency(tree)
            node = tree.search(123)
            tree.delete(node)
            self._assert_ratio_consistency(tree)
        self.assertEqual(tree.get_amir_balance_factor(), 0)

    # ---------- high volume scaling ------------------------------------
    def test_scaling_to_large_tree(self):
        tree = AVLTree()
        for k in range(10000):
            tree.insert(k, k)
            if k % 100 == 0:
                self._assert_ratio_consistency(tree)

        self.assertGreater(tree.get_amir_balance_factor(), 0)

        keys = list(range(10000))
        random.shuffle(keys)
        for k in keys:
            node = tree.search(k)
            tree.delete(node)
            if k % 100 == 0:
                self._assert_ratio_consistency(tree)

        self.assertEqual(tree.get_amir_balance_factor(), 0)

    # ---------- alternating insertions and deletions --------------------
    def test_alternating_operations(self):
        tree = AVLTree()
        for k in range(1, 501):
            tree.insert(k, k)
            node = tree.search(k)
            tree.delete(node)
            self._assert_ratio_consistency(tree)
        self.assertEqual(tree.get_amir_balance_factor(), 0)

    # ---------- random mixed operations with duplicates and negatives ---
    def test_random_mixed_operations(self):
        tree = AVLTree()
        keys_in_tree = set()
        rng = random.Random(42)

        for _ in range(2000):
            key = rng.randint(-500, 500)

            if key in keys_in_tree and rng.random() < 0.5:
                node = tree.search(key)
                tree.delete(node)
                keys_in_tree.remove(key)
            else:
                if tree.search(key) is not None:
                    continue
                tree.insert(key, key)
                keys_in_tree.add(key)

            if rng.random() < 0.1:
                self._assert_ratio_consistency(tree)

        # Clean‑up: delete remaining keys
        for key in list(keys_in_tree):
            node = tree.search(key)
            tree.delete(node)
            self._assert_ratio_consistency(tree)

        self._assert_ratio_consistency(tree)
        self.assertEqual(tree.get_amir_balance_factor(), 0)


if __name__ == "__main__":
    unittest.main()

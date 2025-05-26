import unittest
from AVLTree import AVLTree


class TestInsertDeleteReturnValues(unittest.TestCase):
    # """
    # Verify that AVLTree.insert and AVLTree.delete return

    #     (# of height updates on the path to the root)
    #     + 1 per single rotation (LL / RR)
    #     + 2 per double rotation (LR / RL)
    # """

    # ---------- INSERT -----------------------------------------------------------------
    def test_insert_root_returns_zero(self):
        tree = AVLTree()
        self.assertEqual(tree.insert(10, "root"), 0)

    def test_insert_child_height_update(self):
        tree = AVLTree()
        tree.insert(10, "root")
        self.assertEqual(tree.insert(5, "leaf"), 1)                 # 1 height update, no rotations

    def test_insert_rr_single_rotation(self):
        tree = AVLTree()
        tree.insert(10, "a")                                         # 0
        self.assertEqual(tree.insert(20, "b"),1)                                # 1
        self.assertEqual(tree.insert(30, "c"), 2)                    # 1 height + 1 L-rotation

    def test_insert_ll_single_rotation(self):
        tree = AVLTree()
        tree.insert(20, "a")
        tree.insert(10, "b")
        self.assertEqual(tree.insert(5, "c"), 2)                     # 1 height + 1 R-rotation

    def test_insert_lr_double_rotation(self):
        tree = AVLTree()
        tree.insert(30, "a")
        tree.insert(10, "b")
        self.assertEqual(tree.insert(20, "c"), 3)                    # 1 height + 2 rotations (LR)

    def test_insert_rl_double_rotation(self):
        tree = AVLTree()
        tree.insert(10, "a")
        tree.insert(30, "b")
        self.assertEqual(tree.insert(20, "c"), 3)                    # 1 height + 2 rotations (RL)

    # ---------- DELETE -----------------------------------------------------------------
    def test_delete_leaf_height_update(self):
        tree = AVLTree()
        tree.insert(10, "root")
        tree.insert(5, "leaf")
        node = tree.search(5)
        self.assertEqual(tree.delete(node), 1)                       # root height shrinks by 1

    def test_delete_root_leaf(self):
        tree = AVLTree()
        tree.insert(42, "only")
        node = tree.search(42)
        self.assertEqual(tree.delete(node), 0)                       # remove single-node tree

    def test_delete_root_single_child(self):
        tree = AVLTree()
        tree.insert(10, "root")
        tree.insert(20, "child")
        node = tree.search(10)
        self.assertEqual(tree.delete(node), 0)                       # child promoted, no re-balance

    def test_delete_single_rotation(self):
        # Tree: 10(root) – 5 – 15 – 20  → delete 5 ⇒ single L-rotation
        tree = AVLTree()
        for k in (10, 5, 15, 20):
            tree.insert(k, str(k))
        node = tree.search(5)
        self.assertEqual(tree.delete(node), 1)                       # 1 rotation


    def test_delete_double_rotation(self):
        # Tree: 3(root) – 1 – 5 / 4  → delete 1 ⇒ RL double rotation
        tree = AVLTree()
        for k in (3, 1, 5, 4):
            tree.insert(k, str(k))
        node = tree.search(1)
        self.assertEqual(tree.delete(node), 2)                       # 2 rotations, no height updates

    def test_insert_fourth_no_rotation(self):
        tree = AVLTree()
        self.assertEqual(tree.insert(10, "a"), 0)
        self.assertEqual(tree.insert(20, "b"), 1)
        self.assertEqual(tree.insert(30, "c"), 2)
        self.assertEqual(tree.insert(40, "d"), 2)  # height stabilized, no rotation

    def test_delete_fourth_height_update_only(self):
        tree = AVLTree()
        tree.insert(10, "a")
        tree.insert(20, "b")
        tree.insert(30, "c")
        tree.insert(40, "d")
        node = tree.search(40)
        self.assertEqual(tree.delete(node), 2)  # single height update, no rotation

    def test_insert_height_updates_two_levels(self):
    #     """
    #     20
    #    /  \
    #   10  30
    #   ↓
    #   5         (adds 5 as 10’s left child)

    #     • height(10) rises 0→1
    #     • height(20) rises 1→2
    #     → 2 height updates, no rotations
    #     """
        tree = AVLTree()
        for k in (20, 10, 30):
            tree.insert(k, str(k))
        self.assertEqual(tree.insert(5, "x"), 2)

    # ------------------------------------------------------------------ #
    # INSERT: perfect H=2 tree → add leaf that doesn’t reach the root   #
    # ------------------------------------------------------------------ #
    def test_insert_balanced_leaf_single_height_update(self):
        # """
        # Perfect tree (7 nodes, H=2).  Insert under 10:
        #           40
        #     ┌─────┴─────┐
        #    20           60
        #  ┌─┴─┐       ┌─┴─┐
        # 10 30      50  70
        # """
        full = (40, 20, 60, 10, 30, 50, 70)
        tree = AVLTree()
        for k in full:
            tree.insert(k, str(k))
        self.assertEqual(tree.insert(5, "leaf"), 3)

    # ------------------------------------------------------------------ #
    #  DELETE: two-level height ripple, no rotations                     #
    # ------------------------------------------------------------------ #
    def test_delete_leaf_two_level_height_updates(self):
        # """
        # Using the tree from test_insert_height_updates_two_levels,
        # delete the same leaf (5):

        #   • height(10): 1→0
        #   • height(20): 2→1
        #   → 2 height updates, balanced all the way, no rotations
        # """
        tree = AVLTree()
        for k in (20, 10, 30, 5):
            tree.insert(k, str(k))
        node = tree.search(5)
        self.assertEqual(tree.delete(node), 2)

    # ------------------------------------------------------------------ #
    #  DELETE: root becomes left-heavy → single **right** rotation       #
    # ------------------------------------------------------------------ #
    def test_delete_triggers_right_rotation(self):
        tree = AVLTree()
        for k in (20, 10, 5, 30):
            tree.insert(k, str(k))
        node = tree.search(30)
        self.assertEqual(tree.delete(node), 2)

    # ------------------------------------------------------------------ #
    #  INSERT: 3-height ripple + rotations inside a subtree              #
    # ------------------------------------------------------------------ #
    def test_insert_double_rotation_one_level_below_root(self):
        # """
        # Build a balanced tree        Then insert 45 to make node 50 ‘LR’:

        #          30                             30
        #     ┌────┴────┐                  ┌──────┴─────┐
        #    10        50      →          10            45
        #              / \                               / \
        #             40 60                            40  50
        #                                                  \
        #                                                   60

        # """
        tree = AVLTree()
        for k in (30, 10, 50, 40, 60):
            tree.insert(k, str(k))
        self.assertEqual(tree.insert(45, "x"), 4)


if __name__ == "__main__":
    unittest.main()

import unittest
from AVLTree import AVLNode, AVLTree

#In order to run this test:
#  1. this file should be in the same directory as AVLTree.py.
#  2. run this file using the command: python AVLTester.py
#  3. Note: this test is not exhaustive and does not cover all edge cases.

# Good luck! 

class SimpleAVLTester(unittest.TestCase):

    def setUp(self):
        self.tree = AVLTree()

    def test_insert_and_search(self):
        """Test basic insert and search functionality."""
        self.tree.insert(10, "ten")
        self.tree.insert(20, "twenty")
        self.tree.insert(5, "five")

        self.assertEqual(self.tree.search(10).value, "ten", "FAIL - Search for key 10 failed")
        self.assertEqual(self.tree.search(20).value, "twenty", "FAIL - Search for key 20 failed")
        self.assertEqual(self.tree.search(5).value, "five", "FAIL - Search for key 5 failed")
        self.assertIsNone(self.tree.search(15), "FAIL - Search for non-existent key 15 should return None")

    def test_delete(self):
        """Test basic delete functionality."""
        self.tree.insert(10, "ten")
        self.tree.insert(20, "twenty")
        self.tree.insert(5, "five")

        self.tree.delete(self.tree.search(10))
        self.assertIsNone(self.tree.search(10), "FAIL - Key 10 should be deleted")
        self.assertIsNotNone(self.tree.search(20), "FAIL - Key 20 should still exist")
        self.assertIsNotNone(self.tree.search(5), "FAIL - Key 5 should still exist")

    def test_size(self):
        """Test size functionality."""
        self.assertEqual(self.tree.size(), 0, "FAIL - Size of empty tree should be 0")
        self.tree.insert(10, "ten")
        self.assertEqual(self.tree.size(), 1, "FAIL - Size should be 1 after one insertion")
        self.tree.insert(20, "twenty")
        self.assertEqual(self.tree.size(), 2, "FAIL - Size should be 2 after two insertions")
        self.tree.delete(self.tree.search(10))
        self.assertEqual(self.tree.size(), 1, "FAIL - Size should be 1 after one deletion")

    def test_avl_to_array(self):
        """Test avl_to_array functionality."""
        self.tree.insert(10, "ten")
        self.tree.insert(20, "twenty")
        self.tree.insert(5, "five")
        result = self.tree.avl_to_array()
        expected = [(5, "five"), (10, "ten"), (20, "twenty")]
        self.assertEqual(result, expected, "FAIL - avl_to_array is incorrect")

    def test_get_root(self):
        """Test get_root functionality."""
        self.assertIsNone(self.tree.get_root, "FAIL - Root of an empty tree should be None")
        self.tree.insert(10, "ten")
        self.assertEqual(self.tree.get_root.key, 10, "FAIL - Root key should be 10")
        self.tree.insert(5, "five")
        self.assertEqual(self.tree.get_root.key, 10, "FAIL - Root key should still be 10 after inserting 5")

    def test_amir_balance_factor(self):
        """Test Amir's balance factor."""
        self.assertEqual(self.tree.get_amir_balance_factor(), 0, "FAIL - Amir's balance factor of an empty tree should be 0")
        self.tree.insert(10, "ten")
        self.tree.insert(20, "twenty")
        self.tree.insert(5, "five")
        self.assertEqual(self.tree.get_amir_balance_factor(), 1.0, "FAIL - Amir's balance factor should be 1.0 for a balanced tree")

if __name__ == '__main__':
    unittest.main()
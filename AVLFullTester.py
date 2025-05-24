# AVLFullTester.py

import sys
from AVLTree import AVLTree, AVLNode
# Attempt to import printree for visual dumps
try:
    from printree import printree
    HAS_PRINTREE = True
except ImportError:
    HAS_PRINTREE = False

# ANSI color codes
GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

def print_tree_on_error(tree, msg=None):
    """Print tree visually (if possible) and in-order list."""
    if msg:
        print(f"\nDEBUG ({msg}):")
    if HAS_PRINTREE:
        printree(tree.get_root())
    else:
        # Fallback: in-order list
        arr = tree.avl_to_array()
        print("In-order:", arr)
    print()

def run_test(name, func):
    """Run a single test, print colored pass/fail, dump tree on failure."""
    try:
        func()
        print(f"{GREEN}{name} ✅ GOOD{RESET}")
    except AssertionError as e:
        print(f"{RED}{name} ❌ FAIL: {e}{RESET}")
        # If it's a tree-related error, attempt to dump
        try:
            tree = func.__globals__.get('tree', None)
            if not tree:
                tree = func.__globals__.get('t', None)
            if tree:
                print_tree_on_error(tree, name)
        except Exception:
            pass

# --- Test implementations ---

def test_empty_tree():
    global tree
    tree = AVLTree()
    assert tree.get_root is None, "get_root should be None on empty"
    assert tree.size() == 0, "size should be 0 on empty"
    assert tree.avl_to_array() == [], "avl_to_array should be [] on empty"
    assert tree.search(42) is None, "search on empty should return None"

def test_single_insert_search():
    global tree
    tree = AVLTree()
    tree.insert(10, "ten")
    node = tree.search(10)
    assert node is not None and node.get_value() == "ten", "insert/search failed"
    assert tree.size() == 1, "size should be 1 after insert"
    assert tree.get_root.key == 10, "root key should be 10 after insert"

def test_overwrite_insert():
    global tree
    tree = AVLTree()
    tree.insert(5, "five")
    tree.insert(5, "FIVE")
    node = tree.search(5)
    assert node.get_value() == "FIVE", "insert overwrite failed"
    assert tree.size() == 1, "size should remain 1 after overwrite"

def test_avl_to_array_sorted():
    global tree
    tree = AVLTree()
    for k in [20, 10, 30, 5, 15]:
        tree.insert(k, str(k))
    arr = tree.avl_to_array()
    keys = [k for k,_ in arr]
    assert keys == sorted(keys), "avl_to_array not sorted"

def test_predecessor_successor():
    global tree
    tree = AVLTree()
    for k in [15, 10, 20, 5, 12, 18, 25]:
        tree.insert(k, str(k))
    n12 = tree.search(12)
    pred = tree.get_predecessor(n12)
    succ = tree.get_successor(n12)
    assert pred and pred.key == 10, "predecessor of 12 wrong"
    assert succ and succ.key == 15, "successor of 12 wrong"
    # boundaries
    assert tree.get_predecessor(tree.search(5)) is None, "predecessor of min should be None"
    assert tree.get_successor(tree.search(25)) is None, "successor of max should be None"

def test_delete_leaf_and_internal():
    global tree
    tree = AVLTree()
    for k in [10, 5, 15, 3, 7]:
        tree.insert(k, str(k))
    # delete leaf
    leaf = tree.search(3)
    tree.delete(leaf)
    assert tree.search(3) is None, "leaf deletion failed"
    # delete node with one child
    tree.delete(tree.search(5))
    assert tree.search(5) is None, "one-child deletion failed"
    # delete root with two children
    root = tree.get_root
    tree.delete(root)
    assert tree.search(10) is None, "two-child root deletion failed"

def test_rotations_count():
    global tree
    tree = AVLTree()
    # This sequence causes LL rotation at root
    c1 = tree.insert(30, "30")
    c2 = tree.insert(20, "20")
    c3 = tree.insert(10, "10")  # LL rotate
    assert c3 == 1, "LL rotation count should be 1"
    # RR rotation
    tree = AVLTree()
    tree.insert(10,"10"); tree.insert(20,"20")
    c = tree.insert(30,"30")  # RR rotate
    assert c == 1, "RR rotation count should be 1"
    # LR rotation
    tree = AVLTree()
    tree.insert(30,"30"); tree.insert(10,"10")
    c = tree.insert(20,"20")  # LR = 2
    assert c == 2, "LR rotation count should be 2"
    # RL rotation
    tree = AVLTree()
    tree.insert(10,"10"); tree.insert(30,"30")
    c = tree.insert(20,"20")  # RL = 2
    assert c == 2, "RL rotation count should be 2"

def test_amir_balance_factor():
    global tree
    tree = AVLTree()
    assert tree.get_amir_balance_factor() == 0.0, "empty tree balance factor != 0"
    tree.insert(10,"10"); tree.insert(20,"20"); tree.insert(5,"5")
    # This sequence yields a balanced tree
    bf = tree.get_amir_balance_factor()
    assert 0.0 <= bf <= 1.0, "balance factor out of range"
    # perfect balance test
    tree = AVLTree()
    for k in [20,10,30]:
        tree.insert(k,str(k))
    assert tree.get_amir_balance_factor() == 1.0, "perfectly balanced factor != 1"

def test_mass_insert_delete():
    global tree
    tree = AVLTree()
    N = 100
    for i in range(N):
        tree.insert(i,str(i))
    assert tree.size() == N, "mass insert size wrong"
    for i in range(N):
        tree.delete(tree.search(i))
    assert tree.size() == 0, "mass delete size wrong"
    assert tree.avl_to_array() == [], "avl_to_array not empty after deletes"

# --- Run all tests ---
if __name__ == "__main__":
    tests = [
        test_empty_tree,
        test_single_insert_search,
        test_overwrite_insert,
        test_avl_to_array_sorted,
        test_predecessor_successor,
        test_delete_leaf_and_internal,
        test_rotations_count,
        test_amir_balance_factor,
        test_mass_insert_delete,
    ]
    for test in tests:
        run_test(test.__name__, test)

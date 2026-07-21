"""
Topic: Linked List
Exercise: Reverse Linked List (LeetCode 206) & Merge Two Sorted Lists (LeetCode 21)

Problem Description:
1. `reverse_list(head)`: Reverse a singly linked list in O(N) time and O(1) space.
2. `merge_two_lists(list1, list2)`: Merge two sorted linked lists into one sorted list.

Example 1 (Reverse):
Input: 1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 5 -> 4 -> 3 -> 2 -> 1 -> None

Example 2 (Merge):
Input: 1 -> 2 -> 4, 1 -> 3 -> 4
Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4
"""

from typing import Optional, List

class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverses a singly-linked list iteratively.
    """
    prev = None
    curr = head
    
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
        
    return prev

def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merges two sorted linked lists into a single sorted list.
    """
    dummy = ListNode(-1)
    tail = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    tail.next = list1 if list1 else list2
    return dummy.next

# Helpers for testing
def create_linked_list(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    curr = head
    while curr:
        result.append(curr.val)
        curr = curr.next
    return result

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Linked List...")
    
    # Test 1: Reverse List
    ll1 = create_linked_list([1, 2, 3, 4, 5])
    rev = reverse_list(ll1)
    assert linked_list_to_list(rev) == [5, 4, 3, 2, 1]
    
    # Test 2: Merge Two Sorted Lists
    l1 = create_linked_list([1, 2, 4])
    l2 = create_linked_list([1, 3, 4])
    merged = merge_two_lists(l1, l2)
    assert linked_list_to_list(merged) == [1, 1, 2, 3, 4, 4]
    
    print("All tests passed successfully!")

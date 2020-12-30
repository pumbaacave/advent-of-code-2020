from __future__ import annotations
from typing import List, Optional, Set, Tuple, Dict
from dataclasses import dataclass


def format(num, l):
    # possible return val: [1, l]
    # normal module contaisn [0, l - 1]
    return (num - 1) % l + 1


global M
M: int = 1000000


@dataclass
class Node:
    num: int
    next_node: Optional[Node]

    def __repr__(self) -> str:
        return f"Node: val->{self.num}, next_node: {self.next_node.num}"


def print_link_list(head: Node, list_l):
    while head and list_l:
        list_l -= 1
        print(head.num)
        head = head.next_node


def find_by_val(start: Node, val: int, end: Node):
    # time complexicty: O(N)
    cur = start
    while cur and cur is not end:
        if cur.num == val:
            return cur
        else:
            cur = cur.next_node


def pop_next(node: Node) -> Node:
    # the list is circular, thus no check for nullness
    next_node = node.next_node
    node.next_node = next_node.next_node
    # next_node.next_node = None
    return next_node


def insert(dest: Node, node: Node):
    old_next = dest.next_node
    dest.next_node = node
    node.next_node = old_next


def play(head: Node, list_l: int, val_map: Dict[int, Node]) -> Node:
    cur = head
    pickup_val = set()
    for _ in range(10*M):
        a = pop_next(cur)
        b = pop_next(cur)
        c = pop_next(cur)
        pickup_val.add(a.num)
        pickup_val.add(b.num)
        pickup_val.add(c.num)
        n = format(cur.num - 1, list_l)
        while n in pickup_val:
            n = format(n-1, list_l)
        # print(pickup_val)
        # print(f"cur val: {cur.num}")
        # print(f"dest: {n}")
        dest = val_map[n]
        insert(dest, c)
        insert(dest, b)
        insert(dest, a)
        pickup_val.clear()
        cur = cur.next_node
    # print_link_list(head, list_l)
    one = val_map[1]
    x = one.next_node.num
    y = one.next_node.next_node.num
    print(x, y)
    print(x * y)


if __name__ == "__main__":
    # input = "389125467"
    input = "158937462"
    nums = list(map(int, list(input)))
    head: Node = Node(0, None)
    cur = head
    val_map = dict()
    for n in nums:
        next_node = Node(n, None)
        if cur.num == 0:
            cur = next_node
            head = cur
            val_map[cur.num] = cur
            continue
        cur.next_node = next_node
        cur = next_node
        val_map[cur.num] = cur
    for i in range(10, M + 1):
        next_node = Node(i, None)
        cur.next_node = next_node
        cur = next_node
        val_map[cur.num] = cur

    # create cycle
    cur.next_node = head
    print(val_map[M])
    play(head, M, val_map)

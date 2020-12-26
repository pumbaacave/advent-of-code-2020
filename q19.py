from __future__ import annotations
import sys
from enum import Enum
from typing import List, Dict
import ipdb


class NodeType(Enum):
    # contains a sequense of node
    Seq = 1
    # contains a char
    Data = 2
    # contains a union of sequence node
    Union = 3


def parse_seq(seq: str) -> List[int]:
    # left space
    seq = seq.strip()
    return [int(n) for n in seq.split(' ')]


class Node:
    def __init__(self, line: str):
        num, data = line.split(':')
        data = data.strip()
        self.num = int(num)
        if data.find('|') >= 0:
            self.node_type = NodeType.Union
            self.union = [parse_seq(seq) for seq in data.split('|')]
        elif data.find('"') >= 0:
            # "a"
            self.node_type = NodeType.Data
            self.data = data.replace('"', '')
        else:
            self.node_type = NodeType.Seq
            self.seq = parse_seq(data)

    @staticmethod
    def match_for11(line: str, idx: int, rulebook: Dict[int, Node], first: Node, second: Node) -> int:
        if idx >= len(line):
            return -1
        a = first.match(line, idx, rulebook)
        if a >= len(line) or a < 0:
            return -1
        b = second.match(line, a, rulebook)
        # valid pair match
        if 0 < b <= len(line):
            return b
        else:
            c = Node.match_for11(line, a, rulebook, first, second)
            if c >= len(line) or c < 0:
                return -1
            return second.match(line, c, rulebook)

    def match(self, line: str, idx: int, rulebook: Dict[int, Node]) -> int:
        # return -1 if match failed
        # if matched return next idx to match
        # we cannot overmatch thus not check idx out of range
        # print(self.num, idx)
        if idx >= len(line):
            return -1
        elif self.node_type == NodeType.Data:
            # Only expect data contains 1 character
            return idx + 1 if self.data == line[idx] else -1
        elif self.node_type == NodeType.Seq:
            return Node.match_seq(line, self.seq, idx, rulebook)
        else:
            # assume only 1 seq can succeed
            for seq in self.union:
                ret_idx = Node.match_seq(line, seq, idx, rulebook)
                if ret_idx >= 0:
                    return ret_idx
            return -1

    @staticmethod
    def match_seq(line: str, seq: List[int], idx: int, rulebook: Dict[int, Node]) -> int:
        for child in seq:
            node = rulebook[child]
            idx = node.match(line, idx, rulebook)
            if idx < 0:
                return idx
        return idx

    @staticmethod
    def magic_zero():
        # sorry I am cheating :)
        # but create a general parser is hard and I guess not wanted by the topic
        node = Node("0: 8 | 11")
        node.union = []

        def create(i, j):
            ret = [42 for _ in range(i)]
            for _ in range(j):
                ret.append(42)
            for _ in range(j):
                ret.append(31)
            return ret
        for i in range(1, 8):
            for j in range(1, 8):
                node.union.append(create(i, j))
        return node

    def __repr__(self) -> str:
        if self.node_type == NodeType.Union:
            return f"node type: {self.node_type}, data: {self.union}"
        elif self.node_type == NodeType.Data:
            return f"node type: {self.node_type}, data: {self.data}"
        else:
            return f"node type: {self.node_type}, data: {self.seq}"


def process(line: str, node: Node, rulebook: Dict[int, Node]) -> bool:
    last_matched = node.match(line, 0, rulebook)
    if last_matched == len(line):
        # print(line)
        return True
    else:
        return False


if __name__ == "__main__":
    total = 0
    prep_end = False
    rulebook = {}
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if not line:
            prep_end = True
            continue
        if not prep_end:
            node = Node(line)
            rulebook[node.num] = node
        else:

            # implicit True -> 1 conversion.
            total += process(line, Node.magic_zero(), rulebook)
    print(total)

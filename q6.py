import sys
from typing import List, Set


def count_group(group: List[str]) -> int:
    ans = set()
    for line in group:
        for ch in line:
            ans.add(ch)
    return len(ans)


def count_group_consensus(group: List[str]) -> int:
    if len(group) == 1:
        return len(set(group[0]))
    consensus: Set[str] = set(group[0])
    for line in group[1:]:
        consensus = consensus.intersection(line)
    return len(consensus)


if __name__ == "__main__":
    group: List[str] = []
    total = 0
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if len(line) == 0:
            total += count_group_consensus(group[:])
            group.clear()
        else:
            group.append(line)
    if group:
        total += count_group_consensus(group[:])
    print(total)

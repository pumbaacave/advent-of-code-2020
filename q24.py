import sys
from typing import Tuple, Dict, List, Set
from collections import Counter
from math import sqrt

# sw + ne = (0, 0, 0), means sw and ne can cancel each other upon origin
# sw + nw = w
# need real geometry
# sq3 = sqrt(3)
# sq3 = 1.732
# directions_map = {"e": (2, 0), "se": (1, -sq3), "sw": (-1, -sq3),
#                  "w": (-2, 0), "nw": (-1, sq3), "ne": (1, sq3)}
directions_map = {"e": (2, 0), "se": (1, -1), "sw": (-1, -1),
                  "w": (-2, 0), "nw": (-1, 1), "ne": (1, 1)}


def sum_coord(a: Tuple[int, int], b: Tuple[int, int]) -> \
        Tuple[int, int]:
    return (a[0]+b[0], a[1]+b[1])


def line_to_coord(line: str) -> Tuple[int, int]:
    coord = (0, 0)
    pre = None
    token = ""
    for ch in line:
        if ch in ("n", "s"):
            pre = ch
            continue
        if pre:
            token = pre + ch
            pre = None
        else:
            token = ch
        assert len(token) <= 2
        # print(token)
        coord = sum_coord(coord, directions_map[token])
    return coord


def get_neighbours(cood: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [sum_coord(cood, v) for v in directions_map.values()]


def test_setup():
    sum1 = sum_coord(directions_map["sw"], directions_map["ne"])
    assert sum1 == (0, 0)
    assert sum(sum1) == 0
    sum2 = sum_coord(directions_map["w"], directions_map["e"])
    assert sum2 == (0, 0)
    assert sum(sum2) == 0
    sum3 = sum_coord(directions_map["se"], directions_map["nw"])
    assert sum3 == (0, 0)
    assert sum(sum3) == 0
    sum4 = sum_coord(directions_map["sw"], directions_map["nw"])
    assert sum4 == directions_map["w"]
    sum6 = sum_coord(directions_map["se"], directions_map["ne"])
    assert sum6 == directions_map["e"]
    assert line_to_coord("nwwswee") == (0, 0)
    assert line_to_coord("esew") in get_neighbours((0, 0))


test_setup()


def count_black(cnts: List[int]):
    return sum(1 for num in cnts if num % 2 == 1)


def convey(blacks: Set[Tuple[int, int]]):
    whites = set()
    new_blacks = set()
    for b in blacks:
        total1 = 0
        for nei in get_neighbours(b):
            if nei in blacks:
                total1 += 1
            else:
                whites.add(nei)
        if 1 <= total1 <= 2:
            new_blacks.add(b)
    for w in whites:
        total2 = 0
        for nei in get_neighbours(w):
            if nei in blacks:
                total2 += 1
        if total2 == 2:
            new_blacks.add(w)
    return new_blacks


if __name__ == "__main__":
    cnt: Dict[Tuple[int, int], int] = Counter()
    for line in sys.stdin.readlines():
        line = line.rstrip()
        cnt[line_to_coord(line)] += 1
    blacks = set(k for k, v in cnt.items() if v % 2 == 1)
    print(len(blacks))
    for _ in range(100):
        blacks = convey(blacks)
    print(len(blacks))

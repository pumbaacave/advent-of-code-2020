from ast import parse
import sys
from typing import Deque, Dict, List, Set
from collections import defaultdict, deque
from pprint import PrettyPrinter
global pp
pp = PrettyPrinter()


def parse_rule(line: str, rulebook: Dict[str, List[int]]):
    # rulebook: keyword -> 4 int
    kv = line.split(":")
    key = kv[0]
    fs = kv[1].split(" or ")
    first = fs[0]
    first_start_end = first.split("-")
    second = fs[1]
    second_start_end = second.split("-")
    rulebook[key].append(int(first_start_end[0]))
    rulebook[key].append(int(first_start_end[1]))
    rulebook[key].append(int(second_start_end[0]))
    rulebook[key].append(int(second_start_end[1]))


def parse_ticket(line: str) -> List[int]:
    return list(map(int, line.split(",")))


def check_error(num: int, rulebook: Dict[str, List[int]]) -> int:
    # can use prepocessinig to speed up
    valid = False
    for r in rulebook.values():
        if r[0] <= num <= r[1] or r[2] <= num <= r[3]:
            valid = True
    return 0 if valid else num


def fit(num: int, r: List[int]) -> bool:
    return r[0] <= num <= r[1] or r[2] <= num <= r[3]


def filter_candidate(ticket: List[int], rulebook: Dict[str, List[int]], can: List[Set[str]]):
    # can use prepocessinig to speed up
    for idx, num in enumerate(ticket):
        can[idx] = set(c for c in can[idx] if fit(num, rulebook[c]))
        # for c in can[idx]:
        #    r = rulebook[c]
        #    if r[0] <= num <= r[1] or r[2] <= num <= r[3]:
        #        continue
        #    else:
        #        can[idx].discard(c)


def topo_sort(cans: List[Set[str]]):
    q: Deque[str] = deque()
    seen = set()
    for idx, can in enumerate(cans):
        print(can)
        if len(can) == 1:
            word = list(can)[0]
            q.append(word)
            seen.add(idx)

    while q:
        cur = q.pop()
        for idx, can in enumerate(cans):
            if idx in seen:
                continue
            if cur in can:
                can.discard(cur)
                if len(can) == 1:
                    word = list(can)[0]
                    q.append(word)
                    seen.add(idx)
    return [list(c)[0] for c in cans]


if __name__ == "__main__":
    rulebook: Dict[str, List[int]] = defaultdict(list)
    my: List[int]
    nearby_tickets: List[List[int]] = []
    lines = sys.stdin.readlines()
    stage = 0
    for line in lines:
        # from macOS
        if line == "\n":
            stage += 1
            continue
        if stage == 0:
            parse_rule(line.rstrip(), rulebook)
        elif stage == 1:
            if line.startswith("your ticket:"):
                continue
            # only once
            my = parse_ticket(line)
        else:
            if line.startswith("nearby tickets:"):
                continue
            nearby_tickets.append(parse_ticket(line))

    # pp.pprint(rulebook)
    # pp.pprint(nearby_tickets)
    candidate = [set(rulebook.keys()) for r in rulebook.keys()]
    for t in nearby_tickets:
        if any(check_error(num, rulebook) > 0 for num in t):
            continue
        print(t)
        filter_candidate(t, rulebook, candidate)
    cans = topo_sort(candidate)
    mul = 1
    for field, num in zip(cans, my):
        if field.startswith("departure"):
            mul *= num
    print(mul)
        

from collections import defaultdict
import sys
from typing import List, Tuple, Set, Dict, Final

SEP = "(contains"


def parse_catalog(line: str):
    # be carefult to spaces
    words: List[str] = line[:-2].split(' ')
    allergens = set()
    idx = words.index(SEP)
    ingredients = set(words[:idx])
    for word in words[idx+1:]:
        allergens.add(word.rstrip(','))
    return (ingredients, allergens)


def build_map(data: List[Tuple[Set[str], Set[str]]], i_to_a: Dict[str, str]):
    print("mapping")
    print(i_to_a)
    can = defaultdict(list)
    # solve the mapping from unknow ingredients to allergen
    # maybe need multiple round
    # 1. figure out any mapping 2. eliminate knowns. -> 1
    # new data build from intersection
    for ing, agn in data:
        if len(agn) == 1 and len(ing) == 1:
            # since 1 ingredient can contain at most 1 kind
            # of allergen
            i_to_a[ing.pop()] = agn.pop()
    for i, (in_a, agn_a) in enumerate(data):
        for j, (in_b, agn_b) in enumerate(data[i+1:]):
            new_agn = agn_a.intersection(agn_b)
            if not new_agn:
                continue
            new_in = in_a.intersection(in_b)
            if len(new_agn) == 1:
                if len(new_in) == 1:
                    # since 1 ingredient can contain at most 1 kind
                    # of allergen
                    i_to_a[new_in.pop()] = new_agn.pop()
                elif len(new_in) > 1:
                    can[new_agn.pop()].append(new_in)

    print("possible match")
    print(can)
    for a1, cans in can.items():
        remain = cans[0]
        for c in cans:
            remain = remain.intersection(c)
        # no mutation
        print(remain)
        if(len(remain) == 1):
            i_to_a[list(remain)[0]] = a1
        elif len(remain) > 1:
            b = set()
            b.add(a1)
            data.append((remain, b))

    print(i_to_a)
    for ing, a in data:
        for k, v in i_to_a.items():
            if k in ing:
                ing.discard(k)
                a.discard(v)
    data = [(ing, a) for ing, a in data if a]
    # if len(a) == 1:
    #    # since 1 ingredient can contain at most 1 kind
    #    # of allergen
    #    i_to_a[ing.pop()] = a.pop()
    # ingredient set without allergen provides no info, delete
    # new_data = [(ing, a) for ing, a in new_data if a]
    print(data)
    # return i_to_a
    return i_to_a if not data else build_map(data[:], i_to_a)


def count_safe(data: List[Tuple[Set[str], Set[str]]], i_to_a: Dict[str, str]) \
        -> int:
    total = 0
    for ings, agn in data:
        for ing in ings:
            if ing not in i_to_a:
                total += 1
    return total


def build_canonical_key(i_to_a: Dict[str, str]):
    keys = sorted(i_to_a.keys(), key=lambda k: i_to_a[k])
    return ','.join(keys)


if __name__ == "__main__":
    data = []
    for line in sys.stdin.readlines():
        data.append(parse_catalog(line))
    # print(data)
    i_to_a = build_map(data[:], {})
    print(count_safe(data, i_to_a))
    print(build_canonical_key(i_to_a=i_to_a))

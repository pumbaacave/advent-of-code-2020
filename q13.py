from os import dup
import sys
from typing import Tuple
from math import gcd


def get_leadtime_and_id(start: int, id: int) -> Tuple[int, int]:
    mul, res = divmod(start, id)
    return (id - res, id)


def part1():
    l1 = sys.stdin.readline()
    time = int(l1)
    l2 = sys.stdin.readline()
    ids = map(int, filter(lambda id: id != 'x', l2.split(',')))
    leadtime_departtimes = [
        get_leadtime_and_id(time, id) for id in ids]
    ans = min(leadtime_departtimes)
    print(ans[0] * ans[1])


if __name__ == "__main__":
    _ = sys.stdin.readline()
    l2 = sys.stdin.readline()
    ids = list(map(lambda x: int(x) if x != "x" else 1, l2.split(',')))
    all_gcd = 1
    duration: int = 1
    cur = ids[0]
    for index, id in enumerate(ids):
        # checking the index-th id of bus valid or not
        # if id == 1(from 'x') always true
        # else jump after the whole period to find a fit for current id
        while ((cur + index) % id) != 0:
            cur += duration
        all_gcd = gcd(1, id)
        duration = duration * id // all_gcd
    print(cur)

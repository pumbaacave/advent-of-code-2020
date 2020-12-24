from os import lchflags
import sys
from typing import List, Dict


def game1(nums: List[int], end_turn: int):
    # nums: starting numbers, visibly there are no duplicates in them.
    # may there be any period so that we can take a short cut?
    idx = 1
    # for all numbers
    last_shown_at: Dict[int, int] = dict()
    last_last_shown_at: Dict[int, int] = dict()
    for num in nums:
        last_shown_at[num] = idx
        idx += 1

    print(last_shown_at)
    last_num = nums[-1]
    while idx <= end_turn:
        last_shown = last_shown_at.get(last_num, 0)  # get_or_default
        last_last_shown = last_last_shown_at.get(last_num, 0)  # get_or_default
        # first show
        if last_last_shown == 0:
            num = 0
        else:
            num = last_shown - last_last_shown

        if num == 0:
            print(idx, num)
        # move to l_l_dict, later update l_dict
        last_last_shown_at[num] = last_shown_at.get(num, 0)
        last_shown_at[num] = idx
        last_num = num
        idx += 1
    print(last_shown_at, last_last_shown_at)
    print(idx, last_num)


if __name__ == "__main__":
    nums = map(int, sys.stdin.readline().split(","))
    nums = list(nums)
    game1(nums, 100)

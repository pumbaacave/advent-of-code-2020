import sys
from typing import List, Set
from collections import Counter


def for_Q1():
    # need nums from stdin
    nums.sort()
    cnt = Counter()
    for first, second in zip(nums, nums[1:]):
        cnt[second - first] += 1
    # first num
    cnt[nums[0]] += 1
    # last jolt
    cnt[3] += 1
    print(cnt)
    print(cnt[1] * cnt[3])


def dp_for_3(l: int, m: int, nums: Set[int]):
    state = [0] * (m + 3)
    state[0] = 1
    for i in range(m):
        if(i + 1 in nums):
            state[i + 1] += state[i]
        if(i + 2 in nums):
            state[i + 2] += state[i]
        if(i + 3 in nums):
            state[i + 3] += state[i]
    print(state[m])


if __name__ == "__main__":
    nums: List[int] = list(map(int, sys.stdin.readlines()))
    nums.sort()
    least = nums[0]
    most = nums[-1]
    dp_for_3(least, most, set(nums))

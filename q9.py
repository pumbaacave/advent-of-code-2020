import sys
from typing import List
from collections import Counter


def for_Q1():
    # need nums from stdin
    len_window = 25
    state = Counter()
    # must be a pair
    for i in range(len_window - 1):
        for j in range(i+1, len_window):
            state[nums[i]+nums[j]] += 1
    # check
    for i, num in enumerate(nums[len_window:], len_window):
        if state[num] == 0:
            print(f"invalid number : {num} ")
            break
        for pre in range(i - len_window + 1, i):
            state[nums[pre]+nums[i]] += 1
            state[nums[pre]+nums[i - len_window]] -= 1


def check(left: int, right: int, nums: List[int]):
    print(left, right)
    MIN = float("inf")
    MAX = -float("inf")
    for num in nums[left: right + 1]:
        MIN = min(MIN, num)
        MAX = max(MAX, num)
    print(MAX, MIN)


if __name__ == "__main__":
    # answer for 1st part
    NUM = 18272118
    #NUM = 127
    nums: List[int] = list(map(int, sys.stdin.readlines()))
    total = 0
    acc_sum = []
    # suppose no overflow
    for num in nums:
        total += num
        acc_sum.append(total)
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if acc_sum[j] - acc_sum[i] == NUM:
                check(i, j, nums)

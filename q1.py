import sys
from typing import Tuple, Optional

global nums


def sum2(start: int, end: int, target: int) -> Optional[Tuple[int, int]]:
    """
    Find two number in the nums[start:end] whose sum is equal to target.
    """
    seen = set()
    for i in range(start, end):
        n = nums[i]
        if target - n in seen:
            return (n, (target - n))
        else:
            seen.add(n)
    return None


if __name__ == "__main__":
    nums = sorted(map(int, sys.stdin))
    end = len(nums)
    for i, num in enumerate(nums):
        ret = sum2(i + 1, end, 2020 - num)
        if ret:
            print(num * ret[0] * ret[1])

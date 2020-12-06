import sys
from typing import List


def parse(raw: str, one_token: str, zero_token: str) -> int:
    s1 = raw.replace(one_token, "1")
    s2 = s1.replace(zero_token, "0")
    return int(s2, 2)  # base of 2 integer


def get_id(line: str) -> int:
    row = line[:7]
    col = line[7:]
    r = parse(row, 'B', 'F')
    c = parse(col, 'R', 'L')
    return (r << 3) + c


if __name__ == "__main__":
    ids: List[int] = sorted([get_id(line)for line in sys.stdin.readlines()])
    for front, back in zip(ids, ids[1:]):
        if back - front == 2:
            print(front + 1)

import sys
from typing import List


def num_hit_tree(r: int, down: int, lines: List[str]) -> int:
    col: int = 0
    row: int = 0
    cnt: int = 0
    # newline is not a char we care :)
    # suppose all line are with the same length
    line_len: int = len(lines[0]) - 1
    for line in lines[1::down]:
        #row += 1
        # if row % down != 0:
        #    continue
        col = (col + r) % line_len
        if(line[col] == '#'):
            cnt += 1

    return cnt


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    a = num_hit_tree(3, 1, lines)
    b = num_hit_tree(1, 1, lines)
    c = num_hit_tree(5, 1, lines)
    d = num_hit_tree(7, 1, lines)
    e = num_hit_tree(1, 2, lines)
    print(a, b, c, d, e)
    print(a * b * c * d * e)

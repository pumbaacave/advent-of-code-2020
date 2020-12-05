import sys
#from typing import int


def check_line(line: str) -> int:
    """
    line sample
    6-11 w: sbwwwwwqwmkw
    """
    cmd, target, pw = line.split(' ')
    low, high = cmd.split('-')
    low = int(low)
    high = int(high)
    cnt = pw.count(target.rstrip(':'))
    if cnt:
        return 1 if low <= cnt <= high else 0
    return 0


def check_line_2(line: str) -> int:
    """
    line sample
    6-11 w: sbwwwwwqwmkw
    """
    cmd, target, pw = line.split(' ')
    low, high = cmd.split('-')
    # -1 to offset one base to zero base
    low = int(low) - 1
    high = int(high) - 1
    target = target.rstrip(':')
    # suppose no index out of bound

    first = low < len(pw) and target == pw[low]
    second = high < len(pw) and target == pw[high]
    return 1 if first ^ second else 0


if __name__ == "__main__":
    print(sum(check_line_2(line) for line in sys.stdin))

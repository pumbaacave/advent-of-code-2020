import sys
from typing import List, Dict, Final


def parse_passport(lines: List[str]) -> Dict[str, str]:
    items = [item for line in lines for item in line.split(' ')]
    ret = dict()
    for item in items:
        k, v = item.split(':')
        ret[k] = v.rstrip()
    return ret


def check_valid(passport: Dict[str, str]) -> bool:
    """
    ignore cid
    """
    required: Final[List[str]] = [
        "ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"]
    return all(k in passport for k in required)


def check_range(s: str, low: int, high: int) -> bool:
    if not s.isdecimal():
        return False
    return low <= int(s) <= high


assert check_range("1989", 1920, 2002), "bry fail"


def check_hgt(s: str) -> bool:
    "like: 1cm or 2in"
    if len(s) < 3:
        return False
    if s[-2:] == "cm":
        return check_range(s[:-2], 150, 193)
    if s[-2:] == "in":
        return check_range(s[:-2], 59, 76)
    return False


def check_hcl(s: str) -> bool:
    if len(s) != 7:
        return False
    if s[0] != '#':
        return False
    can = "abcdef"
    for c in s[1:]:
        if not c.isdecimal() and c not in can:
            return False
    return True


global eyes
cons = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
eyes = set(cons)


def check_ecl(s: str) -> bool:
    return s in eyes


def check_pid(s: str) -> bool:
    return len(s) == 9 and s.isdecimal()


def check_valid_2(pp: Dict[str, str]) -> bool:
    """
    ignore cid
    """
    # check key existance first
    if not check_valid(pp):
        return False
    BYR = "byr"
    if not check_range(pp[BYR], 1920, 2002):
        print(BYR + "fail")
        print(pp[BYR])
        return False
    IYR = "iyr"
    if not check_range(pp[IYR], 2010, 2020):
        print(IYR + "fail")
        print(pp[IYR])
        return False
    EYR = "eyr"
    if not check_range(pp[EYR], 2020, 2030):
        print(EYR + "fail")
        print(pp[EYR])
        return False
    HGT = "hgt"
    if not check_hgt(pp[HGT]):
        print(HGT + "fail")
        print(pp[HGT])
        return False
    HCL = "hcl"
    if not check_hcl(pp[HCL]):
        print(HCL + "fail")
        print(pp[HCL])
        return False
    ECL = "ecl"
    if not check_ecl(pp[ECL]):
        print(ECL + "fail")
        print(pp[ECL])
        return False
    PID = "pid"
    if not check_pid(pp[PID]):
        print(PID + "fail")
        print(pp[PID])
        return False
    return True


if __name__ == "__main__":
    buffer: List[str] = []
    passports = []
    for line in sys.stdin:
        if line == '\n':
            passports.append(parse_passport(buffer[:]))
            buffer.clear()
        else:
            buffer.append(line)
    if buffer:
        passports.append(parse_passport(buffer[:]))

    print(sum(map(check_valid_2, passports)))

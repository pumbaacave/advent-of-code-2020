import sys
import re
from pprint import PrettyPrinter
from types import new_class
from typing import Dict, List


global pp
pp = PrettyPrinter()

global mask_p
mask_p = re.compile(r'mask\s=\s(?P<mask>.*)')
memory_p = re.compile(r'mem\[(?P<addr>\d*)\]\s=\s(?P<value>.\d*)')


def parse_mask(line: str):
    result = re.search(mask_p, line)
    if result:
        return result[1]
    else:
        print(f"{line} is not mask parsable")
        return ""


def parse_memory(line: str):
    result = re.search(memory_p, line)
    if result:
        return int(result[1]), int(result[2])
    else:
        print(f"{line} is not memory parsable")
        return 0, 0


def apply_mask(val: int, mask: str):
    # return 1 val applied the mask
    idx: int = 0
    for bit in reversed(mask):
        num = 1 << idx
        if bit == '1':
            val = val | num
        elif bit == '0':
            if val & num:
                val -= num
        idx += 1
    return val


def flat_mask(mask: str, results: List[List[str]]) -> List[List[str]]:
    if not mask:
        return results
    if mask[0] == '0':
        return flat_mask(mask[1:], [m + ['0'] for m in results])
    elif mask[0] == '1':
        return flat_mask(mask[1:], [m + ['1'] for m in results])
    else:  # '+'
        return flat_mask(mask[1:], [m + ['1'] for m in results] +
                         [m + ['0'] for m in results])


def apply_mask_ver2(addr: int, mask: str) -> str:
    # return all resutled val applied the mask
    new_mask = []
    idx: int = 0
    for bit in reversed(mask):
        num = 1 << idx
        if bit == '1':
            new_mask.append('1')
        elif bit == '0':
            new_mask.append(str((addr & num) >> idx))
        else:
            new_mask.append('X')
        idx += 1
    return ''.join(reversed(new_mask))


if __name__ == "__main__":
    mask: str = ""
    m_ss = []
    mem: Dict[int, int] = {}
    for line in sys.stdin.readlines():
        if line.startswith("mask"):
            mask = parse_mask(line)
        else:
            addr, val = parse_memory(line)
            mask_add_addr = apply_mask_ver2(addr, mask)
            # pp.pprint(mask_add_addr)
            # pp.pprint(flat_mask(mask_add_addr, [[]]))
            m_ss = [int(''.join(mem), 2)
                    for mem in flat_mask(mask_add_addr, [[]])]
            # pp.pprint(m_ss)
            for mask_num in m_ss:
                mem[mask_num] = val
    print(sum(mem.values()))

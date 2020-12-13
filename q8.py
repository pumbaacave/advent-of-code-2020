import sys

from dataclasses import dataclass
from typing import List


@dataclass()
class Op:
    code: str
    operant: int


def parse(line: str):
    f, s = line.rstrip().split(' ')
    return Op(f, int(s))


def run(cmds: List[Op]) -> bool:
    idx = 0
    num = 0
    seen = set()
    l = len(cmds)
    while True:
        if idx >= l:
            print("found")
            print(num)
            return True
        if idx in seen:
            print(num)
            return False
        seen.add(idx)
        op = cmds[idx]
        if(op.code == "nop"):
            idx += 1
        if(op.code == "acc"):
            idx += 1
            num += op.operant
        if(op.code == "jmp"):
            idx += op.operant


def tran(op: Op) -> Op:
    if op.code == "nop":
        return Op("jmp", op.operant)
    else:
        return Op("nop", op.operant)


if __name__ == "__main__":
    cmds: List[Op] = []
    for line in sys.stdin.readlines():
        cmds.append(parse(line))
    for i, op in enumerate(cmds):
        if op.code in ("nop", "jmp"):
            new_cmds = cmds[:i] + [tran(op)] + cmds[i+1:]
            run(new_cmds)

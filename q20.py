from __future__ import annotations
import sys
from typing import List
from dataclasses import dataclass


def reverse_str(line):
    n = len(line)
    return line[-1:-n-1:-1]


def create_boarders(tile: List[str]):
    ret = []
    n = len(tile)
    ret.append(tile[0])
    buffer = []
    for i in range(n):
        buffer.append(tile[i][n-1])
    ret.append(''.join(buffer))
    buffer.clear()
    ret.append(reverse_str(tile[n-1]))
    for i in range(n):
        buffer.append(tile[i][0])
    ret.append(''.join(reversed(buffer)))
    return ret


def create_flip_boarders(tile):
    tile = [reverse_str(line) for line in tile]
    return create_boarders(tile)


@dataclass
class Image:
    tile: List[str]
    boarders: List[str]
    flip_boarders: List[str]
    num: int

    def __init__(self, data: List[str]) -> None:
        self.num = int(data[0][5:9])
        self.tile = data[1:]
        self.boarders = create_boarders(self.tile)
        self.flip_boarders = create_flip_boarders(self.tile)

    @property
    def all_boarders(self):
        return set(self.boarders) | set(self.flip_boarders)

    def match(self, other: Image) -> bool:
        return len(self.all_boarders.intersection(other.all_boarders)) > 0


if __name__ == "__main__":
    buffer: List[str] = []
    image_list: List[Image] = []
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if line:
            buffer.append(line)
        else:
            image = Image(buffer[:])
            # print(image)
            image_list.append(image)
            buffer.clear()
    num_friend_image = {}
    mul = 1
    for i, a in enumerate(image_list):
        num_f = 0
        for j, b in enumerate(image_list):
            if i == j:
                continue
            if a.match(b):
                num_f += 1
        num_friend_image[a.num] = num_f
        if num_f == 2:
            mul *= a.num
    print(num_friend_image)
    print(mul)

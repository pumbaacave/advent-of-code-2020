import sys
from typing import List, Tuple
from dataclasses import dataclass
from math import cos, sin, radians


@dataclass
class Direction:
    # for example x: 1, y: 0 means East
    x: int
    y: int


# Operation codes
global N, S, E, W, L, R, F
N, S, E, W, L, R, F = "N", "S", "E", "W", "L", "R", "F"
global DIRECTIONS, DIRECTION_MAP, E_DIR, W_DIR, S_DIR, N_DIR


@dataclass
class Op:
    # S, W ...
    code: str
    operant: int

    def is_turn(self) -> bool:
        return self.code in (L, R)


E_DIR, S_DIR, W_DIR, N_DIR = Direction(1, 0), Direction(
    0, -1), Direction(-1, 0), Direction(0, 1)
# clockwise
DIRECTIONS: List[Direction] = [E_DIR, S_DIR, W_DIR, N_DIR]
DIRECTION_MAP = {E: E_DIR, S: S_DIR, W: W_DIR, N: N_DIR}


def turn_matrix(left_or_right: str, degree: int, cur_direction: Direction) -> Direction:
    # clockwise will decrement degrees
    if left_or_right == R:
        degree = -degree
    rad = radians(degree)
    # chop off precission error, which did happen for input data
    c = round(cos(rad))
    s = round(sin(rad))
    # x, y must map to integer because degree is multiple of 90
    new_x = cur_direction.x * c - cur_direction.y * s
    new_y = cur_direction.x * s + cur_direction.y * c
    return Direction(int(new_x), int(new_y))


def turn(left_or_right: str, step: int, cur_direction: Direction) -> Direction:
    # Deprecated, use cosine transform ver to avoid fragile index manupalation.
    if left_or_right == L:
        step = -step
    # may raise when data corrupt
    cur_idx: int = DIRECTIONS.index(cur_direction)
    next_idx: int = (cur_idx + step) % 4
    return DIRECTIONS[next_idx]


def parse_op(line: str) -> Op:
    line = line.rstrip()
    return Op(line[0], int(line[1:]))


def move(x: int, y: int, op: Op, cur_direction: Direction) -> Tuple[int, int]:
    if op.code == F:
        x += cur_direction.x * op.operant
        y += cur_direction.y * op.operant
        return (x, y)
    else:
        direction = DIRECTION_MAP[op.code]
        x += direction.x * op.operant
        y += direction.y * op.operant
        return (x, y)


def apply_part1(cmds: List[Op]):
    x, y, direction = 0, 0, E_DIR
    for cmd in cmds:
        print(direction)
        if cmd.is_turn():
            direction = turn_matrix(cmd.code, cmd.operant, direction)
        else:
            x, y = move(x, y, cmd, direction)
    print(x, y)


def turn2(left_or_right: str, degree: int, cur_direction: Direction) -> Direction:
    # Now the norm of cur_direction is no 1 any more.
    # decopose to x-axis (NW), y-axis and combine later, that is how vector geometry works
    # This method is wrong, don't know exactly why tho
    x = cur_direction.x
    x_dir = E_DIR if x > 0 else W_DIR
    y = cur_direction.y
    y_dir = N_DIR if y > 0 else S_DIR
    x_dir = turn_matrix(left_or_right, degree, x_dir)
    y_dir = turn_matrix(left_or_right, degree, y_dir)
    return Direction(x_dir.x * x + y_dir.x * y, x_dir.y * x + y_dir.y * y)


def apply_part2(cmds: List[Op]):
    x, y = 0, 0
    # delta(way point)
    direction = Direction(10, 1)
    for cmd in cmds:
        print(cmd)
        if cmd.is_turn():
            direction = turn_matrix(cmd.code, cmd.operant, direction)
        elif cmd.code == F:
            x += direction.x * cmd.operant
            y += direction.y * cmd.operant
        else:
            d_from_op = DIRECTION_MAP[cmd.code]
            direction = Direction(
                direction.x + d_from_op.x * cmd.operant,
                direction.y + d_from_op.y * cmd.operant)
        print(direction)
    print(x, y)


if __name__ == "__main__":
    cmds: List[Op] = list(map(parse_op, sys.stdin.readlines()))
    apply_part2(cmds)

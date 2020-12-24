import sys
from typing import List
from pprint import PrettyPrinter
pp = PrettyPrinter()


def base(X, Y, Z):
    return [[[INACTIVE for x in range(X)] for y in range(Y)] for z in range(Z)]


def base2(X, Y, Z, W):
    return [[[[INACTIVE for x in range(X)] for y in range(Y)] for z in range(Z)] for w in range(W)]


def contain(Z, Y, X, a, b, c) -> bool:
    return 0 <= a < Z and 0 <= b < Y and 0 <= c < X


def contain2(W, Z, Y, X, a, b, c, d) -> bool:
    return 0 <= a < W and 0 <= b < Z and 0 <= c < Y and 0 <= d < X


global ACTIVE, INACTIVE
ACTIVE: str = '#'
INACTIVE: str = '.'


def cal(i, j, k, boards) -> str:
    # calculate next_boards's i, j, k indexed state base on old boards
    # old board's origin should be offset by (1, 1, 1)
    old_i, old_j, old_k = i - 1, j - 1, k - 1
    # i, j, k
    Z, Y, X = len(boards), len(boards[0]), len(boards[0][0])
    cur = boards[old_i][old_j][old_k] if contain(
        Z, Y, X, old_i, old_j, old_k) else INACTIVE
    num_active = 0
    for a in range(i-1, i+2):
        for b in range(j-1, j+2):
            for c in range(k-1, k+2):
                if a == i and b == j and c == k:
                    # skip current
                    continue
                # state is for next board
                #print(a, b, c)
                #print(Z, Y, X)
                state = boards[a-1][b-1][c-1] if contain(
                    Z, Y, X, a-1, b-1, c-1) else INACTIVE
                if state == ACTIVE:
                    num_active += 1

    if cur == ACTIVE:
        return ACTIVE if num_active in (2, 3) else INACTIVE
    # cur is INACTIVE
    else:
        return ACTIVE if num_active == 3 else INACTIVE


def cal_part2(q, i, j, k, boards) -> str:
    # calculate next_boards's i, j, k indexed state base on old boards
    # old board's origin should be offset by (1, 1, 1)
    old_q, old_i, old_j, old_k = q-1, i - 1, j - 1, k - 1
    # i, j, k
    W, Z, Y, X = len(boards), len(boards[0]), len(
        boards[0][0]), len(boards[0][0][0])
    cur = boards[old_q][old_i][old_j][old_k] if contain2(
        W, Z, Y, X, old_q, old_i, old_j, old_k) else INACTIVE
    num_active = 0
    for a in range(q-1, q+2):
        for b in range(i-1, i+2):
            for c in range(j-1, j+2):
                for d in range(k-1, k+2):
                    if a == q and b == i and c == j and d == k:
                        # skip current
                        continue
                    # state is for next board
                    #print(a, b, c)
                    #print(Z, Y, X)
                    state = boards[a-1][b-1][c-1][d-1] if contain2(
                        W, Z, Y, X, a-1, b-1, c-1, d-1) else INACTIVE
                    if state == ACTIVE:
                        num_active += 1

    if cur == ACTIVE:
        return ACTIVE if num_active in (2, 3) else INACTIVE
    # cur is INACTIVE
    else:
        return ACTIVE if num_active == 3 else INACTIVE


def create_next(boards: List[List[List[str]]]) -> List[List[List[str]]]:
    Z, Y, X = len(boards), len(boards[0]), len(boards[0][0])
    print(Z, Y, X)
    n_boards: List[List[List[str]]] = base(X + 2, Y + 2, Z + 2)
    for i in range(Z + 2):
        for j in range(Y + 2):
            for k in range(X + 2):
                n_boards[i][j][k] = cal(i, j, k, boards)


def create_next_part2(boards: List[List[List[List[str]]]]) -> List[List[List[List[str]]]]:
    W, Z, Y, X = len(boards), len(boards[0]), len(
        boards[0][0]), len(boards[0][0][0])
    n_boards = base2(X + 2, Y + 2, Z + 2, W + 2)
    for q in range(W + 2):
        for i in range(Z + 2):
            for j in range(Y + 2):
                for k in range(X + 2):
                    n_boards[q][i][j][k] = cal_part2(q, i, j, k, boards)
    return n_boards


def print_3d(boards):
    pp.pprint(boards)
    # pp.pprint(nb)


def print_live(boards):
    total = sum(check == ACTIVE for b in boards for line in b for check in line)
    print(total)


def print_live2(hyper_boards):
    total = sum(
        check == ACTIVE for boards in hyper_boards for b in boards for line in b for check in line)
    print(total)


if __name__ == "__main__":
    board = []
    for line in sys.stdin.readlines():
        line = line.rstrip()
        board.append(list(line))
    now = [[board]]
    # pp.pprint(old)
    for i in range(6):
        now = create_next_part2(now)
    print_live2(now)
    # print_3d(now)

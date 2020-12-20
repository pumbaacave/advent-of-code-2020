import sys
import pprint
import copy
from typing import List, Tuple

global pp
pp = pprint.PrettyPrinter()
global EMPTY, FLOOR, OCCUPIED, NEIGHBOURS
EMPTY: str = "L"
FLOOR: str = "."
OCCUPIED: str = "#"
# 8 direction's neighbours
NEIGHBOURS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def get_num_nearby_occupied(i: int, j: int, board: List[List[str]],
                            num_row: int, num_col: int) -> int:
    total: int = 0
    for row_del, col_del in NEIGHBOURS:
        r = row_del + i
        c = col_del + j
        if r < 0 or num_row <= r:
            continue
        if c < 0 or num_col <= c:
            continue
        if board[r][c] == OCCUPIED:
            total += 1
    return total


def mutate_part2(last_board: List[List[str]],
                 num_row: int, num_col: int) -> List[List[str]]:
    # Can be used as direction as well.
    # -1: not init, 0: see an OCCUPIED in the direction
    # 1: see EMPTY in the direction or itself is at border
    dp = [[[-1 for _ in range(num_col)]for _ in range(num_row)]
          for _ in range(8)]

    def depth_first_search(dp_idx, row_del, col_del, i, j):
        # This helper funciton modify outer function's local vars.
        # already computed
        if dp[dp_idx][i][j] > -1:
            return dp[dp_idx][i][j]
        r = i + row_del
        c = j + col_del
        # Base case:
        # current location is at the boarder
        if r < 0 or num_row <= r:
            dp[dp_idx][i][j] = 1
            return 1
        if c < 0 or num_col <= c:
            dp[dp_idx][i][j] = 1
            return 1
        # neighbour itself is a block
        if(last_board[r][c] == OCCUPIED):
            dp[dp_idx][i][j] = 0
            return 0
        # neighbour's visibility of empty seatness can pass in
        elif(last_board[r][c] == EMPTY):
            dp[dp_idx][i][j] = 1
            return 1
        # neighbour must be FLOOR, inherit its view
        else:
            neighbour_state = depth_first_search(
                dp_idx, row_del, col_del, r, c)
            dp[dp_idx][i][j] = neighbour_state
            return neighbour_state

    for dp_idx, (row_del, col_del) in enumerate(NEIGHBOURS):
        for i in range(num_row):
            for j in range(num_col):
                depth_first_search(dp_idx, row_del, col_del, i, j)

    board: List[List[str]] = copy.deepcopy(last_board)
    for i in range(num_row):
        for j in range(num_col):
            if last_board[i][j] == FLOOR:
                continue
            num_occupied = sum(dp[dp_idx][i][j] == 0
                               for dp_idx in range(8))
            if last_board[i][j] == OCCUPIED and num_occupied >= 5:
                board[i][j] = EMPTY
            elif last_board[i][j] == EMPTY and num_occupied == 0:
                board[i][j] = OCCUPIED
    return board


def mutate(last_board: List[List[str]]) -> List[List[str]]:
    # return a new board according to part2's rule.
    # assume board has more than 1 row.
    # copy data to board for mutation
    board = copy.deepcopy(last_board)
    row, col = len(board), len(board[0])
    for i in range(row):
        for j in range(col):
            num_o = get_num_nearby_occupied(i, j, last_board, row, col)
            if last_board[i][j] == EMPTY and num_o == 0:
                board[i][j] = OCCUPIED
            elif last_board[i][j] == OCCUPIED and num_o >= 4:
                board[i][j] = EMPTY
    return board


def get_num_occupied(board: List[List[str]]) -> int:
    return sum(sum(seat == OCCUPIED for seat in row) for row in board)


if __name__ == "__main__":
    # Convey's game adjusted version.
    board: List[List[str]] = [list(line.rstrip()) for line
                              in sys.stdin.readlines()]
    cnt: int = 0
    num_row, num_col = len(board), len(board[0])
    # assume the count will not go up carcy
    while cnt < 1000000:
        next_board: List[List[str]] = mutate_part2(board, num_row, num_col)
        # pp.pprint(next_board)
        if next_board == board:
            break
        else:
            cnt += 1
            board = next_board
    print(cnt)
    print(get_num_occupied(next_board))

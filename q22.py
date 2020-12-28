import sys
from copy import copy
from typing import List, Deque, Tuple, Set
from collections import deque


def build_deck(lines: List[str]):
    # first line is header
    return deque(map(int, lines[1:]))


def play(deck1: Deque[int], deck2: Deque[int]):
    # assume no cards share the same number
    turn = 0
    while deck1 and deck2:
        head1, head2 = deck1.popleft(), deck2.popleft()
        if head1 > head2:
            deck1.append(head1)
            deck1.append(head2)
        else:
            deck2.append(head2)
            deck2.append(head1)
        turn += 1
        # print(f"{turn}: {deck1} \n {deck2}")
    return deck1, deck2


def make_hash(deck1: Deque[int], deck2: Deque[int]) -> str:
    # bad impl
    # str(list(deck1) + list(deck2)) can not distinguish same total order among the 2 players
    return str(deck1) + str(deck2)


global memo, forse_player1_win
forse_player1_win: bool = False
memo = dict()


def play2(deck1: Deque[int], deck2: Deque[int]) -> Tuple[Deque[int], Deque[int]]:
    # return players' deck after the game
    # must implement circuit breaker because infinite loop did occur in my game data
    playbook = set()
    turn = 0
    # print(len(memo))
    while deck1 and deck2:
        turn += 1
        record = make_hash(deck1, deck2)
        # print(record)
        # print(deck1, deck2)
        if record in playbook:
            # empty player2's deck to force player1's victory
            return deck1, deque()
        else:
            playbook.add(record)

        head1, head2 = deck1.popleft(), deck2.popleft()
        len1, len2 = len(deck1), len(deck2)
        if head1 <= len1 and head2 <= len2:
            # start a subgame
            # key = make_hash(deck1, deck2)
            # if key in memo:
            #     sub_deck1, sub_deck2 = memo[key]
            # else:
            #     sub_deck1, sub_deck2 = play2(
            #         deque(list(deck1)[:head1]), deque(list(deck2)[:head2]))
            #     memo[key] = (sub_deck1, sub_deck2)
            sub_deck1, sub_deck2 = play2(
                deque(list(deck1)[:head1]), deque(list(deck2)[:head2]))
            if sub_deck1:
                # player1 win the sub game
                deck1.append(head1)
                deck1.append(head2)
            else:
                deck2.append(head2)
                deck2.append(head1)
            # to next round
            continue

        # old game
        if head1 > head2:
            deck1.append(head1)
            deck1.append(head2)
        else:
            deck2.append(head2)
            deck2.append(head1)
    return deck1, deck2


def score(deck: Deque[int]):
    print(deck)
    total = 0
    for i, card in enumerate(list(deck)[-1:-len(deck) - 1:-1]):
        total += card * (i + 1)
    print(total)


def score2(deck):
    deck = list(deck)
    deck.reverse()
    total = 0
    for i, d in enumerate(deck, 1):
        total += i * d
    print(total)


if __name__ == "__main__":
    buffer: List[str] = []
    deck1: Deque[int] = deque()
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if line:
            buffer.append(line)
        else:
            deck1 = build_deck(buffer)
            buffer.clear()
    deck2 = build_deck(buffer)
    # deck1, deck2 = play2(deck1, deck2)
    d1, d2 = play2(deck1, deck2)
    print(d1, d2)
    score2(d1) if d1 else score2(d2)
# too high: 35865

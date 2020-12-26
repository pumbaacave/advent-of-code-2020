import sys
from token import NEWLINE, NUMBER, OP
from tokenize import TokenInfo, generate_tokens, tokenize
from typing import List, Deque, Tuple
from collections import deque


sys.setrecursionlimit(200)


def my_eval(op: str, args: Deque[int]):
    if op == '*':
        args.appendleft(args.popleft() * args.popleft())
    if op == '+':
        args.appendleft(args.popleft() + args.popleft())
    if op == ')':
        return


def is_prior(op1, op2) -> bool:
    if op1 == '(':
        return True
    return False


def process_p(arg_stack: Deque[int], ops_stack: Deque[str]) -> Tuple[Deque[int], Deque[str]]:
    # need to craft out parenthesis control block termination logic
    # pop '(' first
    ops_stack.popleft()
    a, o = process1(arg_stack, ops_stack)
    if o and o[0] == ')':
        o.popleft()
    return a, o


def eval_binary(op: str, arg_stack: Deque[int], ops_stack: Deque[str]) ->  \
        Tuple[Deque[int], Deque[str]]:
    left = arg_stack.popleft()
    if ops_stack and is_prior(ops_stack[0], op):
        arg_stack, ops_stack = process_p(arg_stack, ops_stack)
    right = arg_stack.popleft()
    if op == '+':
        arg_stack.appendleft(left + right)
    elif op == '*':
        arg_stack.appendleft(left * right)
    else:
        print(f"not binary op: {op}")
    # do not enter process loop, which will turn all operator right assosiative
    return process1(arg_stack, ops_stack)


def eval_binary_part2(op: str, arg_stack: Deque[int], ops_stack: Deque[str]) \
        -> Tuple[Deque[int], Deque[str]]:
    # '+' preceeds '*'
    left = arg_stack.popleft()
    if ops_stack and is_prior(ops_stack[0], op):
        arg_stack, ops_stack = process_p(arg_stack, ops_stack)
    if op == '+':
        right = arg_stack.popleft()
        arg_stack.appendleft(left + right)
    elif op == '*':
        # special treat, no '(' is possibly next
        if ops_stack and ops_stack[0] == '+':
            arg_stack, ops_stack = process1(arg_stack, ops_stack)
        right = arg_stack.popleft()
        arg_stack.appendleft(left * right)
    else:
        print(f"not binary op: {op}")
    # do not enter process loop, which will turn all operator right assosiative
    return process1(arg_stack, ops_stack)


def process1(arg_stack: Deque[int], ops_stack: Deque[str]) -> Tuple[Deque[int], Deque[str]]:
    # print(arg_stack)
    # print(ops_stack)
    if not ops_stack:
        return arg_stack, ops_stack
    first = ops_stack[0]
    if first == '(':
        arg_stack, ops_stack = process_p(arg_stack, ops_stack)
        return process1(arg_stack, ops_stack)
    elif first == ')':
        return arg_stack, ops_stack
    else:
        return eval_binary_part2(ops_stack.popleft(), arg_stack, ops_stack)


def cal(tokens: List[TokenInfo]) -> int:
    ops_stack = deque()
    arg_stack = deque()
    for t in tokens:
        if t.exact_type == NUMBER:
            arg_stack.append(int(t.string))
        if t.type == OP:
            ops_stack.append(t.string)
    a, o = process1(arg_stack, ops_stack)
    return a[0]


if __name__ == "__main__":
    buffer = []
    total = 0
    for token in generate_tokens(sys.stdin.readline):
        if token.type != NEWLINE:
            buffer.append(token)
        else:
            res = cal(buffer[:])
            total += res
            buffer.clear()
    print(total)

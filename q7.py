import sys
from collections import defaultdict, Counter
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Record:
    num: int
    name: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


def parse_line(line: str) -> List[Record]:
    buffer = []
    words = []
    bags = []
    for c in line:
        if c == '.':
            words.append(''.join(buffer))
            break
        if c in (' ', ','):
            words.append(''.join(buffer))
            buffer.clear()
        else:
            buffer.append(c)
    for i, w in enumerate(words):
        if w in ("bags", "bag"):
            token = ' '.join(words[i-2:i])
            if token == 'no other':
                continue
            if(i >= 3 and words[i-3].isdigit()):
                bags.append(Record(int(words[i-3]), token))
            else:
                bags.append(Record(1, token))

    return bags


def check(head: str, rel: Dict[str, List[str]]) -> bool:
    if head not in rel.keys():
        return False
    if 'shiny gold' in rel[head]:
        return True
    if(any(check(tail, rel) for tail in rel[head])):
        return True


def measure(head: Record, rel: Dict[Record, List[Record]], cnt: Counter) -> int:
    if head.name in cnt:
        return cnt[head.name]
    if head not in rel or len(rel[head]) == 0:
        cnt[head.name] = 0
        return 0
    total = sum(tail.num * (measure(tail, rel, cnt) + 1) for tail in rel[head])
    cnt[head.name] = total
    return total


if __name__ == "__main__":
    rel = defaultdict(list)
    cnt = Counter()
    for line in sys.stdin.readlines():
        # relation: Tuple[str, List[str]] = parse_line(line)
        rel1 = parse_line(line)
        # build multi map
        if rel1:
            rel[rel1[0]].extend(rel1[1:])
    for k in rel:
        measure(k, rel, cnt)
    print(cnt['shiny gold'])

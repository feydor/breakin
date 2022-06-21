from dataclasses import dataclass
from functools import reduce

@dataclass
class Level:
    rows: int = 0
    cols: int = 0
    targets: list[list[bool]] = None

def level(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    level = Level()
    level.rows = len(lines)
    level.cols = max(map(len, lines))
    level.targets = [[False for x in range(level.cols)] for y in range(level.rows)]

    for i,line in enumerate(lines):
        for j,c in enumerate(line[:-1]):
            level.targets[i][j] = True if c == 'X' else False
            None

    return level
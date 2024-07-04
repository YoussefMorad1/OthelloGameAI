from enum import Enum


class Colors(Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2

    @property
    def InverseColor(self):
        if self == Colors.EMPTY:
            return Colors.EMPTY
        elif self == Colors.WHITE:
            return Colors.BLACK
        return Colors.WHITE


class AIDifficulty(Enum):
    EASY = 1
    MEDIUM = 3
    HARD = 5
    VERYHARD = 7

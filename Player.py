from Piece import Piece
from utils import STARTING_POSITIONS
import random


class Player:
    def __init__(self, color: str, start: int, home_column_start: int, winning_position: int):
        self.pieces = [Piece(i, color, STARTING_POSITIONS[color][i]) for i in range(4)]
        self.color = color
        self.start = start
        self.home_column_start = home_column_start
        self.winning_position = winning_position

    def roll_dice(self):
        return random.randint(1, 6)

from Player import Player
from Piece import Piece
from utils import PLAYER_STARTS, HOME_COLUMN_STARTS, WINNING_POSITIONS


class Board:
    def __init__(self, num_players):
        self.players: list[Player] = []
        self.num_players = num_players
        self.initialize_players()

    def initialize_players(self):
        colors = ["Green", "Blue", "Red", "Yellow"]
        for i in range(self.num_players):
            self.add_player(colors[i], PLAYER_STARTS[colors[i]], HOME_COLUMN_STARTS[colors[i]], WINNING_POSITIONS[colors[i]])

    def add_player(self, color, start, home_column_start, winning_position):
        self.players.append(Player(color, start, home_column_start, winning_position))

    def move_piece(self, player_index: int, piece_index, roll):
        player = self.players[player_index]
        piece: Piece = player.pieces[piece_index]
        moved = False

        # Calculate the raw new position without considering rollover or home column
        raw_new_position = piece.position + roll

        # Handle rollover when going over 51
        rollover_new_position = (raw_new_position) % 52

        # 0. Check if the piece is in the winning position
        if piece.position == player.winning_position:
            new_position = player.winning_position
            moved = False

        # 1. Entering the common area
        elif piece.position == piece.start_position:
            if roll == 6 or roll == 1:
                new_position = player.start
            else:
                new_position = piece.start_position

        # 2. Entering the home row
        elif piece.position <= player.home_column_start and raw_new_position >= player.home_column_start:
            new_position = raw_new_position + 100
        # 3. Entering the winning position
        elif raw_new_position > player.home_column_start and raw_new_position > 100:
            if raw_new_position >= player.winning_position:
                new_position = player.winning_position
            else:
                new_position = raw_new_position
        else:
            new_position = rollover_new_position

        # 4. Landing in a piece of the same color
        self.crowning_logic(player, piece, new_position)

        # 5. Landing in a piece of a different color
        self.capture_logic(player, piece, new_position)

        # Update the piece's position
        if piece.position != new_position:
            moved = True
        self.move_crowned_logic(piece, new_position)
        piece.position = new_position
        return moved

    def crowning_logic(self, player: int, piece: Piece, new_position):
        for p in player.pieces:
            if p == piece:
                continue
            if p.position == new_position:
                p.crown_members.add(piece)
                piece.crown_members.add(p)

    def capture_logic(self, player: int, piece: Piece, new_position):
        for p in self.players:
            if p.color == player.color:
                continue
            for enemy_piece in p.pieces:
                if enemy_piece.position == new_position:
                    enemy_piece.position = enemy_piece.start_position
                    for pic in enemy_piece.crown_members:
                        pic.position = pic.start_position
                        pic.crown_members = set()
                    enemy_piece.crown_members = set()
                    break

    def move_crowned_logic(self, piece: Piece, new_position):
        for pic in piece.crown_members:
            pic.position = new_position

    def check_winner(self, player_index: int):
        player = self.players[player_index]

        # Check if all pieces have reached the winning position
        if all(piece.position == player.winning_position for piece in player.pieces):
            return True
        return False

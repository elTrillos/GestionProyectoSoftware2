from Player import Player
from Piece import Piece

PLAYER_STARTS = {
    "Green": 0,
    "Yellow": 13,
    "Blue": 26,
    "Red": 39
}


HOME_COLUMN_STARTS = {
    "Green": 50,
    "Yellow": 11,
    "Blue": 24,
    "Red": 37
}

WINNING_POSITIONS = {
    "Green": 996,
    "Yellow": 997,
    "Blue": 998,
    "Red": 999
}


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

    def move_piece_old(self, player_index: int, piece_index, roll):
        player = self.players[player_index]
        piece: Piece = player.pieces[piece_index]

        if piece.home_row:
            # Check if the piece is in the home row
            if piece.position + roll > player.home_column_start + 5:
                piece.position = player.winning_position
                for p in piece.crown_members:
                    p.position = player.winning_position
                return True
            else:
                piece.position = piece.position + roll
                for p in piece.crown_members:
                    p.position = p.position + roll
                return True
        elif piece.position == player.winning_position:
            return False

        # Check if the piece is in the start position
        elif piece.position == piece.start_position:
            if roll == 6 or roll == 1:
                piece.position = player.start
                # check if the piece eats another piece
                for p in self.players:
                    if p.color == player.color:
                        continue
                    for q in p.pieces:
                        if q.position == player.start:
                            q.position = q.start_position
                            q.home_row = False
                            for r in q.crown_members:
                                r.position = r.start_position
                                r.home_row = False
                                r.crown_members = set()
                            q.crown_members = set()
                            break
                return True
            return False
        else:
            # Calculate the new position
            new_position = piece.position + roll

            # Check if a piece will pass by the cell that enters the home row
            # if the piece is not in the home row
            # and the piece will pass by the cell that enters the home row
            if piece.position < player.home_column_start and new_position >= player.home_column_start:
                new_position = new_position + 100
                piece.home_row = True
            else:
                if new_position > player.home_column_start and piece.home_row:
                    # if start + roll is greater than the last cell in the home row
                    # then the piece will reach the winning position
                    new_position = player.winning_position
                else:
                    # if start + roll is less than the last cell in the home row
                    # then the piece will just move forward
                    new_position = new_position

            # Check if the new position is occupied by another piece of a different color
            for p in self.players:
                if p.color == player.color:
                    continue
                for q in p.pieces:
                    if q.position == new_position:
                        q.position = q.start_position
                        q.home_row = False
                        for r in q.crown_members:
                            r.position = r.start_position
                            r.home_row = False
                            r.crown_members = set()
                        q.crown_members = set()
                        break

        # Check if the new position is occupied by another piece of the same color
        for p in player.pieces:
            if p.position == new_position:
                piece.crown_members.add(p)
                p.crown_members.add(piece)

        # Update position
        if piece.position == new_position:
            return False

        piece.position = new_position
        for p in piece.crown_members:
            p.position = new_position
        return True

    def move_piece(self, player_index: int, piece_index, roll):
        player = self.players[player_index]
        piece: Piece = player.pieces[piece_index]

        # 0. Check if the piece is in the winning position
        if piece.position == player.winning_position:
            return False

        # Calculate the raw new position without considering rollover or home column
        raw_new_position = piece.position + roll

        # Handle rollover when going over 51
        rollover_new_position = (raw_new_position) % 52

        # 1. Entering the common area
        if piece.position == piece.start_position:
            if roll == 6 or roll == 1:
                piece.position = player.start
                new_position = player.start
            else:
                new_position = piece.start_position
                return False

        # 2. Entering the home row
        elif piece.position < player.home_column_start and rollover_new_position >= player.home_column_start:
            new_position = rollover_new_position + 100
            piece.home_row = True
        # 3. Entering the winning position
        elif rollover_new_position > player.home_column_start and piece.home_row or rollover_new_position == player.home_column_start + 5:
            new_position = player.winning_position
        else:
            new_position = rollover_new_position

        # 4. Landing in a piece of the same color
        self.crowning_logic(player, piece)

        # 5. Landing in a piece of a different color
        self.capture_logic(player, piece)

        # Update the piece's position
        piece.position = new_position
        self.move_crowned_logic(piece, new_position)
        return True

    def crowning_logic(self, player: int, piece: Piece):
        for p in player.pieces:
            if p == piece:
                continue
            if p.position == piece.position:
                p.crown_members.add(piece)
                piece.crown_members.add(p)

    def capture_logic(self, player: int, piece: Piece):
        for p in self.players:
            if p.color == player.color:
                continue
            for enemy_piece in p.pieces:
                if enemy_piece.position == piece.position:
                    enemy_piece.position = enemy_piece.start_position
                    enemy_piece.home_row = False
                    for r in enemy_piece.crown_members:
                        r.position = r.start_position
                        r.home_row = False
                        r.crown_members = set()
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

from Board import Board
import random


class Game:
    def __init__(self, num_players):
        self.board = Board(num_players)
        self.current_player_index = self.select_starting_player()
        self.last_dice_roll = 0

    def select_starting_player(self):
        highest_roll = 0
        highest_roll_player_index = 0

        # Roll dice for each player
        for player_index in range(self.board.num_players):
            current_player = self.board.players[player_index]
            roll = current_player.roll_dice()

            # Check if current player has the highest roll
            if roll > highest_roll:
                highest_roll = roll
                highest_roll_player_index = player_index
        return highest_roll_player_index

    def get_last_dice_roll(self):
        return self.last_dice_roll

    def get_current_player(self):
        return self.board.players[(self.current_player_index - 1) % self.board.num_players]

    def play_turn(self):
        # Get the current player
        current_player = self.board.players[self.current_player_index]

        # Roll the dice for the current player
        roll = current_player.roll_dice()
        self.last_dice_roll = roll
        print(f"Player {current_player.color} rolled a {roll}")

        # Try to move each piece until successful (or could skip this player)
        try_order = [0, 1, 2, 3]
        random.shuffle(try_order)
        for piece_index in range(4):  # Assuming each player has 4 pieces
            if self.board.move_piece(self.current_player_index, try_order[piece_index], roll):
                print(f"Player {current_player.color} successfully moved a piece.")
                break

        for pl in self.board.players:
            print(pl.color)
            print(pl.pieces[0].position, pl.pieces[1].position, pl.pieces[2].position, pl.pieces[3].position)
        print()

        # Check for a winner
        if self.board.check_winner(self.current_player_index):
            print(f"Player {current_player.color} wins!")
            return True

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % self.board.num_players
        return False

from Game import Game  # Make sure to import your Game class


def main():
    # Get the number of players (you can use your get_num_players function here)
    num_players = 4  # For example, for a 2-player game

    # Create a new Game instance with the given number of players
    game = Game(num_players)

    # Start the game
    game.start_game()


if __name__ == "__main__":
    main()

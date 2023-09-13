import random
#from classes import Board, Dice, Piece, Team
from classes.Board import Board
from classes.Dice import Dice
from classes.Piece import Piece
from classes.Team import Team

# Función para jugar una partida de Ludo
def game():
    while True:
        num_players = int(input("Elija la cantidad de jugadores (2-4): "))
        if 2 <= num_players <= 4:
            break
        else:
            print("Cantidad de jugadores inválida. Intente nuevamente.")

    # Estos siempre juegan
    red_team = Team("Red")
    yellow_team = Team("Yellow")
    for i in range(4):
        Piece(f"R{i+1}", red_team, 0, 0, False)
        Piece(f"Y{i+1}", yellow_team, 26, 0, False)

    if num_players == 2:
        playing_teams = [red_team, yellow_team]

    elif num_players == 3:
        blue_team = Team("Blue")
        playing_teams = [red_team, blue_team, yellow_team]
        for i in range(4):
            Piece(f"B{i+1}", blue_team, 13, 0, False)
    else:
        blue_team = Team("Blue")
        green_team = Team("Green")
        playing_teams = [red_team, blue_team, yellow_team, green_team]
        for i in range(4):
            Piece(f"B{i+1}", blue_team, 13, 0, False)
            Piece(f"G{i+1}", green_team, 39, 0, False)

    # Crear el tablero
    board = Board()

    # Crear el dado
    dice = Dice()

    # Parte siempre el primero de la lista
    random.shuffle(playing_teams)
    print(playing_teams[0].color + " Team starts the game.")
    
    while True:
        for team in playing_teams:
            board.print_board()
            print(f"--------------------------------------{team.color} Team's turn.")
            input("Press enter to throw the dice.")

            # Tirar el dado
            movement = dice.throw()
            print(f"The dice threw a {movement}.")

            # Seleccionar una ficha para mover
            piece = team.search_for_piece_in_special_board()
            if piece is not None:
                # Mover la ficha
                piece.team.place_piece_in_special_board(piece, movement)
                piece.move(movement)

                # TODO Verificar si el equipo ganó
                continue
            
            piece = board.search_for_piece_in_common_board(team.color)
            if piece is not None:
                # Mover la ficha
                board.place_piece(piece, movement)
                piece.move(movement)

                # TODO Verificar si el equipo ganó
                continue

            if movement == 6:
                # Seleccionar una ficha para mover
                for piece in team.pieces:
                    if piece.state == False and piece.list_position == 0:
                        break
                # Posicionar la ficha
                board.place_on_starting_cell(piece)
                continue
            
            


# Iniciar el juego
game()

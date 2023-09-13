class Board: #common board
    def __init__(self):
        self.board = [None] * 51

    def place_on_starting_cell(self, piece):
        if piece.team.color == "Red":
            self.board[piece.start_position_index] = piece
        elif piece.team.color == "Blue":
            self.board[piece.start_position_index] = piece
        elif piece.team.color == "Yellow":
            self.board[piece.start_position_index] = piece
        elif piece.team.color == "Green":
            self.board[piece.start_position_index] = piece

        print(piece.name + " has been placed on the starting cell.") # *Debugging

    def place_piece(self, piece, movement):
        current_position = piece.list_position + piece.start_position_index
        if current_position > 50: #en caso de que haya dado vuelta el tablero
            current_position -= 51
        self.board[current_position] = None
        if piece.list_position + movement > 50: 
            piece.team.special_board[piece.list_position + movement- 51] = piece

            print(piece.name + " has been placed on the special board at index " + str(piece.list_position + movement - 51)) # * Debugging
        else:
            landing_position = piece.list_position + piece.start_position_index + movement
            if landing_position > 50: #checkea si con su movimiento aterriza en inicios del common board
                landing_position -= 51

            if self.board[landing_position] is None:
                self.board[landing_position] = piece
            elif self.board[landing_position].team.color != piece.team.color:
                self.board[landing_position].list_position = 0 # Si me como una pieza, la devuelvo a su team
                self.board[landing_position] = piece
            elif self.board[landing_position].team.color == piece.team.color: 
                self.board[landing_position] = [self.board[landing_position], piece] #Este en caso de que caiga una tercera ficha en el mismo lugar se rompe, quedan listas de listas

            print(piece.name + " has been placed on the board at index " + str(landing_position)) # *Debugging

    def search_for_piece_in_common_board(self, team_color):
        for piece in self.board[::-1]: #reversed list
            if piece is not None:
                if piece.team.color == team_color:
                    return piece
        return None
    
    def print_board(self):
        print("Board:")
        print(["-" if piece is None else piece.name for piece in self.board])
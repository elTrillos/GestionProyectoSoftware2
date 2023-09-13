class Team:
    def __init__(self, color):
        self.color = color
        self.special_board = [None] * 6
        self.pieces = []

    def add_piece(self, piece):
        self.pieces.append(piece)
    
    def search_for_piece_in_special_board(self):
        for piece in self.special_board[::-1]: #reversed list
            if piece is not None:
                return piece
        return None
    
    def place_piece_in_special_board(self, piece, movement):
        current_position = piece.list_position - 51

        self.special_board[current_position] = None  
        if piece.list_position + movement > 56: 
            piece.state = True #Significa que esta pieza ya gano
            piece.list_position = 56 #posicion final
        else:
            piece.team.special_board[piece.list_position + movement - 51] = piece

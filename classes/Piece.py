class Piece():
    def __init__(self, name, team, start_position_index, list_position, state): #state es si ya gano esa ficha o no
        self.name = name
        self.team = team
        self.start_position_index = start_position_index
        self.list_position = list_position #posicion en la lista propia, para cada ficha va de 0 a 51 independiente de color, no como el board
        self.state = state
        team.add_piece(self)
    
    def __str__(self):
        return f"Piece {self.name} at list index {self.list_position}"
    
    def move(self, movement_number):
        self.list_position += movement_number
    
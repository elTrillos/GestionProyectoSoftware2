class Piece:
    def __init__(self, id, color, start_position):
        self.id = f"{id}_{color}"
        self.position = start_position
        self.home_row = False
        self.crown_members: set[Piece] = set()
        self.start_position = start_position

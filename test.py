from tkinter import Tk, Canvas
from PIL import Image, ImageTk
from utils import CELL_MAPPINGS
from Player import STARTING_POSITIONS
from Game import Game


game = Game(num_players=2)

# Dictionary to keep track of pieces and their canvas IDs
canvas_pieces = {}


def update_board():
    # Update the board state based on the new game state
    for player in game.board.players:
        for piece in player.pieces:
            cell_number = piece.position
            x, y = CELL_MAPPINGS[cell_number]
            print('Drawing piece', piece.id, 'at', x, y, 'for player', player.color)
            color_fill = player.color
            text_fill = 'white'
            if player.color == "Yellow":
                color_fill = "Gold"
                text_fill = 'black'
            text = str(len(piece.crown_members) + 1)
            for p in canvas_pieces:
                print(p)
            if piece.id not in canvas_pieces:
                # Draw new piece and text
                canvas_id = canvas.create_oval(x, y, x + 40, y + 40, fill=color_fill, outline='black', width=2)
                text_id = canvas.create_text(x + 20, y + 20, text=text, fill=text_fill, font=('Arial', 20))
                canvas_pieces[piece.id] = {'piece': canvas_id, 'text': text_id}
            else:
                # Update the position of an existing piece and text
                canvas_id = canvas_pieces[piece.id]['piece']
                text_id = canvas_pieces[piece.id]['text']
                canvas.coords(canvas_id, x, y, x + 40, y + 40)
                canvas.coords(text_id, x + 20, y + 20)
                canvas.itemconfig(text_id, text=text)


def on_key_press(event):
    if event.keysym == 'Escape':
        root.quit()
        return

    update_board()

    # Play one turn of the game
    game_over = game.play_turn()
    # For example, roll the dice, move the piece, check for a winner, etc.
    print("Key pressed")
    # Update the board

    if game_over:
        # Display a message
        canvas.create_text(400, 900, text="Game Over!", fill='black', font=('Arial', 40))
        print("Game Over!")
        # Stop listening for keypresses
        root.unbind("<Key>")


# Initialize the Tkinter window
root = Tk()
root.title('Ludo Game')

# Create a canvas to draw the board
canvas = Canvas(root, width=800, height=1000, bg='white')
canvas.pack()

# Load and display the image
image = Image.open("mel/assets/board.jpg")
image = image.resize((800, 800))
photo = ImageTk.PhotoImage(image)
canvas.create_image(400, 400, image=photo)

# Draw some example pieces (you'll replace this with actual game state)
# for cell in CELL_MAPPINGS:
#     canvas.create_oval(CELL_MAPPINGS[cell][0], CELL_MAPPINGS[cell][1], CELL_MAPPINGS[cell][0] + 40, CELL_MAPPINGS[cell][1] + 40, fill='pink', outline='black', width=2)

# for color in STARTING_POSITIONS:
#     for i in range(4):
#         x, y = STARTING_POSITIONS[color][i]
#         color_fill = color
#         if color == "Yellow":
#             color_fill = "Gold"
#         canvas.create_oval(x, y, x + 40, y + 40, fill=color_fill.lower(), outline='black', width=2)
#         canvas.create_text(x + 20, y + 20, text=str(1), fill='white', font=('Arial', 20))

# Bind keypress event to root window
root.bind("<Key>", on_key_press)

# Show the window
root.mainloop()

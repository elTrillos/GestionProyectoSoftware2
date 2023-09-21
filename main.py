from tkinter import Tk, Canvas, Label, Button
from PIL import Image, ImageTk
from utils import CELL_MAPPINGS
from Game import Game
import sys
import os

# Determine if running as a packaged application
if getattr(sys, 'frozen', False):
    # If packaged
    base_path = sys._MEIPASS
else:
    # If running as normal Python script
    base_path = os.path.dirname(__file__)


def update_board(color: str):
    # Clear the canvas
    canvas.delete("all")

    # Redraw the board
    canvas.create_image(400, 400, image=photo)

    # Update the board state based on the new game state
    for player in game.board.players:
        for piece in player.pieces:
            cell_number = piece.position
            x, y = CELL_MAPPINGS[cell_number]
            color_fill = player.color
            text_fill = 'white'
            if player.color == "Yellow":
                color_fill = "Gold"
                text_fill = 'black'
            text = str(len(piece.crown_members) + 1)
            # Draw new piece and text
            canvas.create_oval(x, y, x + 40, y + 40, fill=color_fill, outline='black', width=2)
            canvas.create_text(x + 20, y + 20, text=text, fill=text_fill, font=('Arial', 20))
    canvas.create_text(250, 900, text=f"{color} dice roll", fill='black', font=('Arial', 30))
    canvas.create_image(450, 900, image=dice_images[game.get_last_dice_roll() - 1])


def on_key_press(event):
    if event.keysym == 'Escape':
        root.quit()
        return

    color = game.get_current_player().color

    # Play one turn of the game
    game_over = game.play_turn()

    # Update the board
    update_board(color)

    if game_over:
        # Display a message
        text_over = canvas.create_text(400, 700, text="Game Over!", fill='white', font=('Arial', 120))
        bbox = canvas.bbox(text_over)
        rect_item = canvas.create_rectangle(bbox, outline="magenta", fill="black", width=4)
        canvas.tag_raise(text_over, rect_item)

        text_over = canvas.create_text(400, 900, text=f"{game.get_current_player().color} wins!", fill='white', font=('Arial', 120))
        bbox = canvas.bbox(text_over)
        rect_item = canvas.create_rectangle(bbox, outline="magenta", fill="black", width=4)
        canvas.tag_raise(text_over, rect_item)
        # Stop listening for keypresses
        root.unbind("<Key>")


def start_game(num_players):
    global game
    # Close the selection window
    selection_window.quit()
    selection_window.destroy()

    # Initialize the game with the selected number of players
    game = Game(num_players=num_players)


# Create a new Tkinter window for player selection
selection_window = Tk()
selection_window.title("Select Number of Players")

label = Label(selection_window, text="Select number of players:", font=("Helvetica", 24))
label.pack(pady=20)


def create_button(num):
    return Button(
        selection_window,
        text=f"{num} Players",
        command=lambda: start_game(num),
        font=("Helvetica", 18),
        width=10,
        height=2,
    )


button2 = create_button(2)
button3 = create_button(3)
button4 = create_button(4)

button2.pack(pady=10)
button3.pack(pady=10)
button4.pack(pady=10)

selection_window.mainloop()


# Initialize the Tkinter window
root = Tk()
root.title('Ludo Game')

# Create a canvas to draw the board
canvas = Canvas(root, width=800, height=1000, bg='white')
canvas.pack()

# Load and display the image
image = Image.open(os.path.join(base_path, "assets", "board.jpg"))
image = image.resize((800, 800))
photo = ImageTk.PhotoImage(image)
canvas.create_image(400, 400, image=photo)

dice_images = []
for n in range(6):
    image = Image.open(os.path.join(base_path, "assets", f"Alea_{n + 1}.png"))
    image = image.resize((100, 100))
    dice_images.append(ImageTk.PhotoImage(image))

# Bind keypress event to root window
root.bind("<Key>", on_key_press)

# Show the window
root.mainloop()

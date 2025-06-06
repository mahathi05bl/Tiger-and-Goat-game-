import tkinter as tk
from tkinter import messagebox

# ---------------- Global Variables ----------------
root = tk.Tk()
root.title("Tiger and Goat Game")
root.geometry("700x700")
root.configure(bg="#5b3c88")

grid_size = 5
spacing = 100
turn = "Goat"
tiger_positions = []
goat_positions = []
points = {}
point_coords = {}
selected_piece = None
highlighted_moves = []
goats_placed = 0
max_goats = 20
goats_killed = 0

def reset_highlights():
    for move in highlighted_moves:
        game_canvas.delete(move)
    highlighted_moves.clear()

player1_name = ""
player2_name = ""
player_side = {"Player 1": "", "Player 2": ""}

# Define these before using them in Radiobuttons
player1_side_var = tk.StringVar(value="Tiger")
player2_side_var = tk.StringVar(value="Goat")

# ---------------- First Page: Welcome ----------------
first_page = tk.Frame(root, bg="#5b3c88", width=700, height=700)
first_page.pack(fill="both", expand=True)

welcome_label = tk.Label(first_page, text="Welcome to Tiger and Goat Game", font=("Arial", 28, "bold"), fg="white", bg="#5b3c88")
welcome_label.place(relx=0.5, rely=0.3, anchor="center")

play_button = tk.Button(first_page, text="Play", font=("Arial", 18), command=lambda: show_setup())
play_button.place(relx=0.5, rely=0.5, anchor="center")

# ---------------- Second Page: Player Setup ----------------

setup_page = tk.Frame(root, bg="#5b3c88", width=700, height=700)

# Container to center content
setup_container = tk.Frame(setup_page, bg="#5b3c88")
setup_container.place(relx=0.5, rely=0.5, anchor="center")

# Player 1 name entry
player1_label = tk.Label(setup_container, text="Player 1 Name:", font=("Arial", 16), bg="#5b3c88", fg="white")
player1_label.pack(pady=(10, 2))
player1_entry = tk.Entry(setup_container, font=("Arial", 16))
player1_entry.pack(pady=(0, 10))

# Player 2 name entry
player2_label = tk.Label(setup_container, text="Player 2 Name:", font=("Arial", 16), bg="#5b3c88", fg="white")
player2_label.pack(pady=(10, 2))
player2_entry = tk.Entry(setup_container, font=("Arial", 16))
player2_entry.pack(pady=(0, 20))

# Side selection label
side_label = tk.Label(setup_container, text="Choose your sides:", font=("Arial", 16), bg="#5b3c88", fg="white")
side_label.pack(pady=(10, 10))

# Player 1 side selection
player1_frame = tk.Frame(setup_container, bg="#5b3c88")
player1_frame.pack(pady=5)
tk.Label(player1_frame, text="Player 1: ", font=("Arial", 14), bg="#5b3c88", fg="white").pack(side="left")
tk.Radiobutton(player1_frame, text="🐅 Tiger", variable=player1_side_var, value="Tiger", font=("Arial", 14),
               bg="#5b3c88", fg="white", selectcolor="#5b3c88").pack(side="left")
tk.Radiobutton(player1_frame, text="🐐 Goat", variable=player1_side_var, value="Goat", font=("Arial", 14),
               bg="#5b3c88", fg="white", selectcolor="#5b3c88").pack(side="left")

# Player 2 side selection
player2_frame = tk.Frame(setup_container, bg="#5b3c88")
player2_frame.pack(pady=5)
tk.Label(player2_frame, text="Player 2: ", font=("Arial", 14), bg="#5b3c88", fg="white").pack(side="left")
tk.Radiobutton(player2_frame, text="🐅 Tiger", variable=player2_side_var, value="Tiger", font=("Arial", 14),
               bg="#5b3c88", fg="white", selectcolor="#5b3c88").pack(side="left")
tk.Radiobutton(player2_frame, text="🐐 Goat", variable=player2_side_var, value="Goat", font=("Arial", 14),
               bg="#5b3c88", fg="white", selectcolor="#5b3c88").pack(side="left")

# Start button
start_button = tk.Button(setup_container, text="Start", font=("Arial", 18), command=lambda: start_game())
start_button.pack(pady=20)

# ---------------- Game Page ----------------
game_page = tk.Frame(root, bg="#5b3c88")
game_canvas = tk.Canvas(game_page, width=600, height=600, bg="white")
game_canvas.pack(pady=10)
game_status = tk.Label(game_page, text="", font=("Arial", 16), fg="white", bg="#5b3c88")
game_status.pack()

# ---------------- Helper Functions ----------------
def show_setup():
    first_page.pack_forget()
    setup_page.pack(fill="both", expand=True)

def start_game():
    global player1_name, player2_name, player_side

    # Get player names from input fields
    player1_name = player1_entry.get().strip()
    player2_name = player2_entry.get().strip()

    # Validate that both names are entered
    if not player1_name or not player2_name:
        messagebox.showerror("Missing Info", "Please enter both player names.")
        return

    # Validate that players have chosen different sides
    if player1_side_var.get() == player2_side_var.get():
        messagebox.showerror("Invalid Selection", "Both players cannot select the same side!")
        return

    # Store the sides chosen
    player_side = {}  # Ensure it's defined
    player_side["Player 1"] = player1_side_var.get()
    player_side["Player 2"] = player2_side_var.get()

    # Switch to game page
    setup_page.pack_forget()
    game_page.pack(fill="both", expand=True)

    # Initialize game
    draw_board()
    place_initial_tigers()
    update_status()

    # Bind mouse click to game board
    game_canvas.bind("<Button-1>", on_canvas_click)


def draw_board():
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = j * spacing + 50, i * spacing + 50
            points[(j, i)] = (x, y)
            game_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
    for (x1, y1) in points.values():
        for (x2, y2) in points.values():
            if abs(x1 - x2) <= spacing and abs(y1 - y2) <= spacing:
                game_canvas.create_line(x1, y1, x2, y2, fill="gray")

def place_initial_tigers():
    for pos in [(0, 0), (4, 0), (0, 4), (4, 4)]:
        x, y = points[pos]
        oval = game_canvas.create_oval(x-20, y-20, x+20, y+20, fill="orange", tags="tiger")
        point_coords[oval] = pos
        tiger_positions.append(pos)

def update_status():
    global turn
    current_player = player1_name if player_side["Player 1"] == turn else player2_name
    game_status.config(text=f"Turn: {turn} ({current_player}) | Goats Placed: {goats_placed}/{max_goats} | Goats Killed: {goats_killed}")

def is_occupied(pos):
    return pos in tiger_positions or pos in goat_positions

def get_middle_point(start, end):
    return ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)

def move_canvas_piece(item, new_pos):
    x, y = points[new_pos]
    game_canvas.coords(item, x - 20, y - 20, x + 20, y + 20)

def remove_goat(pos):
    global goats_killed
    for piece, p in point_coords.items():
        if p == pos and "goat" in game_canvas.gettags(piece):
            game_canvas.delete(piece)
            goat_positions.remove(pos)
            goats_killed += 1
            break

def get_valid_tiger_moves(tiger_pos):
    moves = []
    x, y = tiger_pos
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if (nx, ny) in points:
                if abs(dx) <= 1 and abs(dy) <= 1 and not is_occupied((nx, ny)):
                    moves.append((nx, ny))
                elif abs(dx) == 2 or abs(dy) == 2:
                    mid = get_middle_point((x, y), (nx, ny))
                    if mid in goat_positions and not is_occupied((nx, ny)):
                        moves.append((nx, ny))
    return moves

def get_valid_goat_moves(goat_pos):
    moves = []
    x, y = goat_pos
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if (nx, ny) in points and not is_occupied((nx, ny)):
                moves.append((nx, ny))
    return moves

def highlight_moves(moves):
    reset_highlights()
    for pos in moves:
        x, y = points[pos]
        dot = game_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline="blue", width=2)
        highlighted_moves.append(dot)

def check_game_over():
    if goats_killed >= 5:
        winner = player1_name if player_side["Player 1"] == "Tiger" else player2_name
        messagebox.showinfo("Game Over", f"Congratulations! Tiger ({winner}) wins!")
        root.destroy()
        return True
    if all(not get_valid_tiger_moves(pos) for pos in tiger_positions):
        winner = player1_name if player_side["Player 1"] == "Goat" else player2_name
        messagebox.showinfo("Game Over", f"Congratulations! Goat ({winner}) wins!")
        root.destroy()
      
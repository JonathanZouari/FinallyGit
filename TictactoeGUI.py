"""Tic-Tac-Toe GUI. Run: python TictactoeGUI.py"""

import tkinter as tk
from tkinter import messagebox
from Tictactoe import winner, board_full, minimax, empty_cells

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        
        self.board = [""] * 9
        self.human_mark = "X"
        self.computer_mark = "O"
        self.vs_computer = False
        self.game_over = False
        self.current_turn = "X"
        
        self.setup_menu()
        
    def setup_menu(self):
        """Setup the initial menu"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(frame, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        mode_label = tk.Label(frame, text="Choose Game Mode:", font=("Arial", 12), bg="#f0f0f0")
        mode_label.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        two_player_btn = tk.Button(
            btn_frame, 
            text="Two Players", 
            font=("Arial", 12),
            width=15,
            command=lambda: self.start_game(vs_computer=False)
        )
        two_player_btn.pack(pady=5)
        
        vs_computer_btn = tk.Button(
            btn_frame, 
            text="vs Computer", 
            font=("Arial", 12),
            width=15,
            command=lambda: self.setup_mark_choice()
        )
        vs_computer_btn.pack(pady=5)
        
    def setup_mark_choice(self):
        """Ask player which mark they want to play as"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = tk.Label(frame, text="Choose Your Mark", font=("Arial", 14, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        x_btn = tk.Button(
            btn_frame, 
            text="Play as X (goes first)", 
            font=("Arial", 12),
            width=20,
            command=lambda: self.start_game(vs_computer=True, human_mark="X")
        )
        x_btn.pack(pady=5)
        
        o_btn = tk.Button(
            btn_frame, 
            text="Play as O", 
            font=("Arial", 12),
            width=20,
            command=lambda: self.start_game(vs_computer=True, human_mark="O")
        )
        o_btn.pack(pady=5)
        
    def start_game(self, vs_computer=False, human_mark="X"):
        """Start a new game"""
        self.board = [""] * 9
        self.vs_computer = vs_computer
        self.human_mark = human_mark
        self.computer_mark = "O" if human_mark == "X" else "X"
        self.game_over = False
        self.current_turn = "X"
        
        self.setup_game_board()
        
        # If computer is X and goes first
        if self.vs_computer and self.computer_mark == "X":
            self.root.after(500, self.computer_move)
    
    def setup_game_board(self):
        """Setup the game board UI"""
        self.clear_window()
        
        # Top frame with info
        top_frame = tk.Frame(self.root, bg="#e0e0e0", height=50)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if self.vs_computer:
            info_text = f"You: {self.human_mark} | Computer: {self.computer_mark}"
        else:
            info_text = f"Current Turn: {self.current_turn}"
        
        self.info_label = tk.Label(top_frame, text=info_text, font=("Arial", 12), bg="#e0e0e0")
        self.info_label.pack(pady=10)
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg="black", padx=2, pady=2)
        board_frame.pack(padx=10, pady=10)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                index = i * 3 + j
                btn = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=5,
                    height=2,
                    bg="white",
                    command=lambda idx=index: self.on_button_click(idx)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
        
        # Bottom frame with buttons
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        new_game_btn = tk.Button(
            bottom_frame,
            text="New Game",
            font=("Arial", 10),
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        menu_btn = tk.Button(
            bottom_frame,
            text="Main Menu",
            font=("Arial", 10),
            command=self.setup_menu
        )
        menu_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(
            bottom_frame,
            text="Quit",
            font=("Arial", 10),
            command=self.root.quit
        )
        quit_btn.pack(side=tk.RIGHT, padx=5)
    
    def on_button_click(self, index):
        """Handle button click"""
        if self.game_over:
            messagebox.showinfo("Game Over", "Game is over. Start a new game.")
            return
        
        if self.board[index]:
            messagebox.showwarning("Invalid Move", "That square is already taken.")
            return
        
        if self.vs_computer and self.current_turn != self.human_mark:
            messagebox.showwarning("Not Your Turn", "Wait for your turn.")
            return
        
        # Human move
        self.board[index] = self.human_mark
        self.update_button(index)
        
        # Check for winner or draw
        if self.check_game_end():
            return
        
        self.current_turn = self.computer_mark if self.human_mark != self.current_turn else self.human_mark
        
        # Computer move
        if self.vs_computer:
            self.root.after(500, self.computer_move)
        else:
            self.current_turn = "O" if self.current_turn == "X" else "X"
            self.update_info()
    
    def computer_move(self):
        """Make computer move"""
        _, index = minimax(self.board, self.computer_mark, True)
        if index is not None:
            self.board[index] = self.computer_mark
            self.update_button(index)
            
            if self.check_game_end():
                return
            
            self.current_turn = self.human_mark
            self.update_info()
    
    def update_button(self, index):
        """Update button display"""
        row = index // 3
        col = index % 3
        self.buttons[row][col].config(text=self.board[index])
        
        # Color the button
        if self.board[index] == "X":
            self.buttons[row][col].config(fg="blue")
        elif self.board[index] == "O":
            self.buttons[row][col].config(fg="red")
    
    def check_game_end(self):
        """Check if game has ended"""
        found = winner(self.board)
        if found:
            self.game_over = True
            if self.vs_computer:
                if found == self.human_mark:
                    messagebox.showinfo("Game Over", f"You win! {found} wins!")
                else:
                    messagebox.showinfo("Game Over", f"Computer wins! {found} wins!")
            else:
                messagebox.showinfo("Game Over", f"{found} wins!")
            return True
        
        if board_full(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        
        return False
    
    def update_info(self):
        """Update info label"""
        if self.vs_computer:
            info_text = f"You: {self.human_mark} | Computer: {self.computer_mark} | Turn: {self.current_turn}"
        else:
            info_text = f"Current Turn: {self.current_turn}"
        self.info_label.config(text=info_text)
    
    def new_game(self):
        """Start a new game with same settings"""
        if self.vs_computer:
            self.start_game(vs_computer=True, human_mark=self.human_mark)
        else:
            self.start_game(vs_computer=False)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sudoku_board import SudokuBoard
from solve_heuristic import solve_heuristic
from solve_backtracking import solve_backtracking
from generator import generate_sudoku_puzzle
import time


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("600x650")
        self.root.configure(bg="#f0f0f0")

        self.grid, self.fixed_cells = self.generate_new_puzzle()
        self.steps = 0
        self.solve_time = 0
        self.stop_solving = False

        self.create_widgets()

    def generate_new_puzzle(self):
        puzzle, _ = generate_sudoku_puzzle()
        return puzzle, [[cell != 0 for cell in row] for row in puzzle]

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(pady=20)

        self.board = SudokuBoard(self.main_frame, self.grid, self.fixed_cells)
        self.board.grid(row=0, column=0, columnspan=3)

        self.algorithm_var = tk.StringVar(value="backtracking")
        tk.Label(self.main_frame, text="Algorithm:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="e")
        algo_menu = ttk.Combobox(self.main_frame, textvariable=self.algorithm_var, values=["backtracking", "heuristic"], state="readonly")
        algo_menu.grid(row=2, column=1, sticky="w")

        tk.Button(
            self.main_frame,
            text="Solve",
            command=self.solve_puzzle,
            bg="#4caf50",
            fg="white",
            font=("Arial", 10),
            padx=10
        ).grid(row=2, column=2, padx=10)

        tk.Button(
            self.main_frame,
            text="Random",
            command=self.reset_puzzle,
            bg="#ff9800",
            fg="white",
            font=("Arial", 10),
            padx=10
        ).grid(row=3, column=0, padx=10, pady=10)

        tk.Button(
            self.main_frame,
            text="Load from File",
            command=self.load_from_file,
            bg="#2196f3",
            fg="white",
            font=("Arial", 10),
            padx=10
        ).grid(row=3, column=1, padx=10, pady=10)

        tk.Button(
            self.main_frame,
            text="Clear",
            command=self.clear_puzzle,
            bg="#f44336",
            fg="white",
            font=("Arial", 10),
            padx=10
        ).grid(row=3, column=2, padx=10, pady=10)

        tk.Button(
            self.main_frame,
            text="Stop",
            command=self.stop_solving_process,
            bg="#9e9e9e",
            fg="white",
            font=("Arial", 10),
            padx=10
        ).grid(row=5, column=1, padx=10, pady=5)

        self.stats_label = tk.Label(
            self.main_frame,
            text="Steps: 0",
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.stats_label.grid(row=4, column=0, columnspan=3)

    def solve_puzzle(self):
        self.steps = 0
        self.stop_solving = False
        grid_copy = [row[:] for row in self.grid]
        self.solve_time = 0

        algorithm = self.algorithm_var.get()

        if algorithm == "backtracking":
            generator = solve_backtracking(grid_copy, self.increment_steps, step_mode=True)
        else:
            generator = solve_heuristic(grid_copy, self.increment_steps, step_mode=True)

        def run_step():
            if self.stop_solving:
                messagebox.showinfo("Stopped", "Solving was stopped.")
                return
            try:
                next_grid = next(generator)
                self.board.update_grid(next_grid)
                self.stats_label.config(text=f"Steps: {self.steps}")
                self.root.after(50, run_step)
            except StopIteration:
                self.grid = grid_copy
                self.board.update_grid(self.grid)
                self.stats_label.config(text=f"Steps: {self.steps} | Done!")
                messagebox.showinfo("Success", "Sudoku solved successfully!")

        self.root.after(100, run_step)

    def stop_solving_process(self):
        self.stop_solving = True

    def increment_steps(self):
        self.steps += 1

    def reset_puzzle(self):
        self.grid, self.fixed_cells = self.generate_new_puzzle()
        self.board.update_grid(self.grid)
        self.board.set_fixed_cells(self.fixed_cells)
        self.steps = 0
        self.solve_time = 0
        self.stats_label.config(text="Steps: 0")

    def load_from_file(self):
        filepath = filedialog.askopenfilename(
            title="Open Sudoku File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "r") as file:
                    puzzle = [list(map(int, line.strip().split())) for line in file.readlines()]
                if len(puzzle) == 9 and all(len(row) == 9 for row in puzzle):
                    self.grid = puzzle
                    self.fixed_cells = [[cell != 0 for cell in row] for row in self.grid]
                    self.board.update_grid(self.grid)
                    self.board.set_fixed_cells(self.fixed_cells)
                    self.steps = 0
                    self.solve_time = 0
                    self.stats_label.config(text="Steps: 0")
                else:
                    messagebox.showerror("Invalid File", "The selected file does not contain a valid Sudoku puzzle.")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading the file: {e}")

    def clear_puzzle(self):
        for i in range(9):
            for j in range(9):
                if not self.fixed_cells[i][j]:
                    self.grid[i][j] = 0
        self.board.update_grid(self.grid)
        self.steps = 0
        self.solve_time = 0
        self.stats_label.config(text="Steps: 0")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()

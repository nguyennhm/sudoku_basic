import tkinter as tk

class SudokuBoard(tk.Frame):
    def __init__(self, parent, sudoku_grid, fixed_cells):
        super().__init__(parent, bg="#000000")
        self.sudoku_grid = [row[:] for row in sudoku_grid]
        self.fixed_cells = fixed_cells
        self.cells = {}
        self.create_board()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                bg_color = "#dbe5f1" if self.fixed_cells[i][j] else "#ffffff"
                top = 2 if i % 3 == 0 else 1
                left = 2 if j % 3 == 0 else 1
                bottom = 2 if i == 8 else 0
                right = 2 if j == 8 else 0

                frame = tk.Frame(
                    self,
                    width=50,
                    height=50,
                    bg="black",
                    highlightbackground="black",
                    highlightthickness=0,
                    bd=0
                )
                frame.grid(row=i, column=j)
                frame.grid_propagate(False)
                frame.pack_propagate(False)

                entry_frame = tk.Frame(
                    frame,
                    bg="black",
                    highlightthickness=0
                )
                entry_frame.pack(fill="both", expand=True, padx=(left, right), pady=(top, bottom))

                entry = tk.Entry(
                    entry_frame,
                    width=2,
                    font=("Arial", 20),
                    justify="center",
                    bg=bg_color,
                    fg="black",
                    bd=0,
                    relief="flat",
                    state="readonly" if self.fixed_cells[i][j] else "normal"
                )
                entry.pack(expand=True, fill="both")

                if self.sudoku_grid[i][j] != 0:
                    entry.insert(0, str(self.sudoku_grid[i][j]))
                if not self.fixed_cells[i][j]:
                    entry.bind("<KeyRelease>", lambda e, r=i, c=j: self.update_cell(r, c, entry.get()))
                self.cells[(i, j)] = entry

    def update_cell(self, row, col, value):
        try:
            if value == "":
                self.sudoku_grid[row][col] = 0
            elif value.isdigit() and 1 <= int(value) <= 9:
                self.sudoku_grid[row][col] = int(value)
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, value)
            else:
                self.cells[(row, col)].delete(0, tk.END)
                self.sudoku_grid[row][col] = 0
        except:
            self.cells[(row, col)].delete(0, tk.END)
            self.sudoku_grid[row][col] = 0

    def update_grid(self, new_grid):
        self.sudoku_grid = [row[:] for row in new_grid]
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].configure(state="normal")
                self.cells[(i, j)].delete(0, tk.END)
                if self.sudoku_grid[i][j] != 0:
                    self.cells[(i, j)].insert(0, str(self.sudoku_grid[i][j]))
                bg_color = "#dbe5f1" if self.fixed_cells[i][j] else "#ffffff"
                self.cells[(i, j)].configure(bg=bg_color)
                if self.fixed_cells[i][j]:
                    self.cells[(i, j)].configure(state="readonly")

    def set_fixed_cells(self, fixed_cells):
        self.fixed_cells = fixed_cells
        for i in range(9):
            for j in range(9):
                state = "readonly" if self.fixed_cells[i][j] else "normal"
                bg_color = "#dbe5f1" if self.fixed_cells[i][j] else "#ffffff"
                self.cells[(i, j)].configure(state=state, bg=bg_color)

    def get_current_grid(self):
        grid = [[0] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.cells[(i, j)].get()
                grid[i][j] = int(value) if value.isdigit() else 0
        return grid
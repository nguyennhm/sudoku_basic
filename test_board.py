import tkinter as tk
from sudoku_board import SudokuBoard

root = tk.Tk()
grid = [[0]*9 for _ in range(9)]
fixed_cells = [[False]*9 for _ in range(9)]
board = SudokuBoard(root, grid, fixed_cells)
print(type(board))  # Phải là <class 'sudoku_board.SudokuBoard'>
board.grid(row=0, column=0)
root.mainloop()
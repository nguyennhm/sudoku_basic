def check(grid, row, col, num):
    if any(grid[row][x] == num for x in range(9)):
        return False
    if any(grid[x][col] == num for x in range(9)):
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

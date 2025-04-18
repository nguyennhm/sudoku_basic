import random

def generate_sudoku_puzzle(empty_cells=45):
    """
    Tạo một bàn Sudoku hợp lệ với một số ô bị ẩn đi (trống).
    :param empty_cells: Số ô trống muốn tạo ra (thường từ 40 đến 50).
    :return: (bàn Sudoku bị ẩn, lời giải đầy đủ)
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(grid, row, col, num):
        # Kiểm tra hàng và cột
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        # Kiểm tra ô 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def fill_grid():
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if fill_grid():
                                return True
                            grid[row][col] = 0
                    return False
        return True

    # Bước 1: Tạo lưới hoàn chỉnh
    fill_grid()
    solution = [row[:] for row in grid]

    # Bước 2: Xóa ngẫu nhiên các ô
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    for i in range(empty_cells):
        row, col = cells[i]
        grid[row][col] = 0

    return grid, solution

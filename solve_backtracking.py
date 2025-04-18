from check import check

def solve_backtracking(grid, step_callback=lambda: None, step_mode=False):
    def backtrack():
        if all(grid[i][j] != 0 for i in range(9) for j in range(9)):
            return True
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if check(grid, row, col, num):
                            grid[row][col] = num
                            step_callback()
                            if step_mode:
                                yield [row[:] for row in grid]
                            result = yield from backtrack() if step_mode else backtrack()
                            if result:
                                return True
                            grid[row][col] = 0
                            step_callback()
                            if step_mode:
                                yield [row[:] for row in grid]
                    return False
        return True

    if step_mode:
        yield from backtrack()
    else:
        return backtrack()

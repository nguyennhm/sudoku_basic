from check import check

def solve_heuristic(grid, step_callback=lambda: None, step_mode=False):
    def get_possible_values(row, col):
        values = set(range(1, 10))
        for x in range(9):
            values.discard(grid[row][x])
            values.discard(grid[x][col])
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                values.discard(grid[start_row + i][start_col + j])
        return list(values)

    def find_mrv_cell():
        min_values = 10
        best_cell = None
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    values = get_possible_values(row, col)
                    if len(values) < min_values:
                        min_values = len(values)
                        best_cell = (row, col, values)
        return best_cell

    def heuristic():
        if all(grid[i][j] != 0 for i in range(9) for j in range(9)):
            return True
        cell = find_mrv_cell()
        if not cell:
            return False
        row, col, values = cell
        for num in values:
            if check(grid, row, col, num):
                grid[row][col] = num
                step_callback()
                if step_mode:
                    yield [row[:] for row in grid]
                result = yield from heuristic() if step_mode else heuristic()
                if result:
                    return True
                grid[row][col] = 0
                step_callback()
                if step_mode:
                    yield [row[:] for row in grid]
        return False

    if step_mode:
        yield from heuristic()
    else:
        return heuristic()

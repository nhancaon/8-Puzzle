from collections import deque
from queue import PriorityQueue
from queue import LifoQueue


def manhattan_distance(state):
    # Calculate the Manhattan distance heuristic for a given state
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_row = (state[i][j] - 1) // 3
                target_col = (state[i][j] - 1) % 3
                distance += abs(i - target_row) + abs(j - target_col)
    return distance


def generate_successors(current_state):
    successors = []
    empty_row, empty_col = None, None

    # Find the position of the empty tile (0)
    for i in range(3):
        for j in range(3):
            if current_state[i][j] == 0:
                empty_row, empty_col = i, j

    # Define possible moves (up, down, left, right)
    moves = [
        (-1, 0, "down"),
        (1, 0, "up"),
        (0, -1, "right"),
        (0, 1, "left")
    ]

    for dr, dc, move_direction in moves:
        new_row, new_col = empty_row + dr, empty_col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in current_state]
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
            successors.append((new_state, move_direction))

    return successors


def bfs_8_puzzle(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    explored = set()
    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            if tuple(map(tuple, next_state)) not in explored:
                queue.append((next_state, path + [move_direction]))

    return None  # No solution found


def ucs_8_puzzle(initial_state, goal_state):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()

    while not open_set.empty():
        _, current_state, path = open_set.get()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        empty_row, empty_col = None, None
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == 0:
                    empty_row, empty_col = i, j

        moves = [
            (empty_row - 1, empty_col, "down"),
            (empty_row + 1, empty_col, "up"),
            (empty_row, empty_col - 1, "right"),
            (empty_row, empty_col + 1, "left"),
        ]

        for row, col, move_direction in moves:
            if 0 <= row < 3 and 0 <= col < 3:
                new_state = [list(row) for row in current_state]
                new_state[empty_row][empty_col], new_state[row][col] = new_state[row][col], new_state[empty_row][empty_col]
                if tuple(map(tuple, new_state)) not in explored:
                    priority = len(path)
                    open_set.put(
                        (priority, new_state, path + [move_direction]))

    return None  # No solution found


def dfs_8_puzzle(initial_state, goal_state, max_depth=50):
    stack = [(initial_state, [])]
    explored = set()

    while stack:
        current_state, path = stack.pop()
        depth = len(path)

        if depth > max_depth:
            continue  # Skip exploration if max depth is reached

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        # Assuming you have a generate_successors function
        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            if tuple(map(tuple, next_state)) not in explored:
                stack.append((next_state, path + [move_direction]))

    return None


def greedy_best_first_search(initial_state, goal_state):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()

    while not open_set.empty():
        _, current_state, path = open_set.get()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        empty_row, empty_col = None, None
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == 0:
                    empty_row, empty_col = i, j
        moves = [
            (empty_row - 1, empty_col, "down"),
            (empty_row + 1, empty_col, "up"),
            (empty_row, empty_col - 1, "right"),
            (empty_row, empty_col + 1, "left"),
        ]

        for row, col, move_direction in moves:
            if 0 <= row < 3 and 0 <= col < 3:
                new_state = [list(row) for row in current_state]
                new_state[empty_row][empty_col], new_state[row][col] = new_state[row][col], new_state[empty_row][empty_col]
                if tuple(map(tuple, new_state)) not in explored:
                    # Greedy: Consider only the heuristic
                    priority = manhattan_distance(new_state)
                    open_set.put(
                        (priority, new_state, path + [move_direction]))

    return None  # No solution found


def a_star_search(initial_state, goal_state):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()

    while not open_set.empty():
        _, current_state, path = open_set.get()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        empty_row, empty_col = None, None
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == 0:
                    empty_row, empty_col = i, j

        moves = [
            (empty_row - 1, empty_col, "down"),
            (empty_row + 1, empty_col, "up"),
            (empty_row, empty_col - 1, "right"),
            (empty_row, empty_col + 1, "left"),
        ]

        for row, col, move_direction in moves:
            if 0 <= row < 3 and 0 <= col < 3:
                new_state = [list(row) for row in current_state]
                new_state[empty_row][empty_col], new_state[row][col] = new_state[row][col], new_state[empty_row][empty_col]
                if tuple(map(tuple, new_state)) not in explored:
                    priority = len(path) + manhattan_distance(new_state)
                    open_set.put(
                        (priority, new_state, path + [move_direction]))

    return None  # No solution found

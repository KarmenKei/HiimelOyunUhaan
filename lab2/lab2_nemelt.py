import random
from collections import deque


ROWS = 4
COLS = 4
LIVES = 3


CELL_TYPES = ['empty', 'food', 'toy', 'bed', 'bone', 'trap']

class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self._generate_grid()
        self.bone_position = self._find_bone()

    def _generate_grid(self):
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                cell = random.choice(CELL_TYPES)
                row.append(cell)
            grid.append(row)
        return grid

    def _find_bone(self):
        """Return coordinates of the bone"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'bone':
                    return (r, c)

        r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self.grid[r][c] = 'bone'
        return (r, c)

    def display(self):
        for row in self.grid:
            print(row)


class DogAgent:
    def __init__(self, env: Environment):
        self.env = env
        self.position = (0, 0)
        self.lives = LIVES
        self.score = 0
        self.visited = set()

    def move(self, new_pos):
        self.position = new_pos
        r, c = new_pos
        cell = self.env.grid[r][c]

        if cell == 'food':
            self.score += 10
            print(" Ate food: +10 points")
        elif cell == 'toy':
            self.score += 5
            print(" Played: +5 points")
        elif cell == 'bed':
            print(" Slept peacefully.")
        elif cell == 'bone':
            self.score += 50
            print(" Found the bone! +50 points")
        elif cell == 'trap':
            self.lives -= 1
            self.score -= 10
            print(" Hit a trap! -1 life, -10 points")

    def search_for_bone(self):
        """Use BFS to find the bone"""
        print("\n Starting search for bone using BFS...")
        queue = deque([(self.position, [self.position])])
        self.visited.add(self.position)

        while queue:
            pos, path = queue.popleft()
            r, c = pos

            if self.env.grid[r][c] == 'bone':
                print(f" Bone found at {pos} after {len(path)} moves!")
                for step in path:
                    self.move(step)
                return True

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.env.rows and 0 <= nc < self.env.cols and (nr, nc) not in self.visited:
                    self.visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
        print(" Bone not found.")
        return False


def main():
    env = Environment(ROWS, COLS)
    print(" Environment:")
    env.display()

    dog = DogAgent(env)
    dog.search_for_bone()

    print("\nFinal Status:")
    print(f"Score: {dog.score}, Lives: {dog.lives}")

if __name__ == "__main__":
    main()
import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Stack data strcuture - DFS
class DFSFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    # remove in Last In, First Out
    def remove(self):
        if self.empty():
            raise Exception('Empty Frontier')
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Queue data strcuture - BFS
class BFSFrontier(DFSFrontier):
    def remove(self):
        if self.empty():
            raise Exception('Empty Frontier')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# Greedy best-first search
class GBFSFrontier(DFSFrontier):
    
    def __init__(self, goal):
        super(GBFSFrontier, self).__init__ ()
        self.goal = goal

    def manhattan_distance(self, node):
        return abs(self.goal[0]-node.state[0]) + abs(self.goal[1]-node.state[1])

    def remove(self):
        if self.empty():
            raise Exception('Empty Frontier')
        else:
            distances = list(map(lambda n: self.manhattan_distance(n), self.frontier))
            selected_node = distances.index(max(distances))
            node = self.frontier[selected_node]
            self.frontier.pop(selected_node)
            return node

# A* Search
class ASearchFrontier(GBFSFrontier):

    def compute_distance(self, node):
        n = node
        actions = []
        while n.parent is not None:
            actions.append(n.action)
            n = n.parent

        return len(actions)

    def remove(self):
        if self.empty():
            raise Exception('Empty Frontier')
        else:
            distances = list(map(lambda n: self.manhattan_distance(n) + self.compute_distance(n), self.frontier))
            selected_node = distances.index(max(distances))
            node = self.frontier[selected_node]
            self.frontier.pop(selected_node)
            return node

class Maze():

    # Init maze
    def __init__(self, filename, algo_number):
        self.algo_number = algo_number
        
        # Read file and set width, height
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count('A') != 1:
            raise Exception('maze must have exactly one starting point')
        if contents.count('B') != 1:
            raise Exception('maze must have exactly one goal')

        # Determine height and width
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row_wall = [] # array of boolean to keep track of wall blocks
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row_wall.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row_wall.append(False)
                    elif contents[i][j] == ' ':
                        row_wall.append(False)
                    else:
                        row_wall.append(True)
                except IndexError:
                    row_wall.append(True)
            self.walls.append(row_wall)

        self.solution = None

    # Print maze
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    # col is boolean value
                    print('🁢', end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif solution is not None and (i, j) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()
        print()

    def neighbors(self, state):
        row, col = state

        # All possible actions
        candidates = [
            ('up', (row-1, col)),
            ('down', (row+1, col)),
            ('left', (row, col-1)),
            ('right', (row, col+1)),
        ]

        # Ensure actions are valid
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]: # check if value is False (not wall block)
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def solve(self):
        """ Finds solution to maze if one exists """
        
        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just starting point
        start = Node(state=self.start, parent=None, action=None)

        if self.algo_number == 0:
            frontier = DFSFrontier()
            print('Depth-First Search Algorithm was chosen')
        elif self.algo_number == 1:
            frontier = BFSFrontier()
            print('Breadth-First Search Algorithm was chosen')
        elif self.algo_number == 2:
            frontier = GBFSFrontier(self.goal)
            print('Greedy Best-First Search Algorithm was chosen')
        elif self.algo_number == 3:
            frontier = ASearchFrontier(self.goal)
            print('Greedy Best-First Search Algorithm was chosen')
        else:
            frontier = DFSFrontier()
            print('Depth-First Search Algorithm was chosen')

        
        frontier.add(start)

        # Init explore set
        self.explored = set()

        # keep looping until solution
        while True:
            
            if frontier.empty():
                raise Exception('no solution')

            # Choose node from frontier
            self.num_explored += 1
            node = frontier.remove()

            if node.state == self.goal:

                # init arrays to trace back how I found the goal
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if len(sys.argv) < 2:
    sys.exit('Usage: python maze.py maze1.txt [algo_number]')

algo_number = 0

if len(sys.argv) == 3:
    algo_number = sys.argv[2]

print('ALGO NUMBER', int(algo_number))

maze_test = Maze(sys.argv[1], int(algo_number))
print('Maze:')
maze_test.print()
print('Solving...')
maze_test.solve()
print('States explored: ', maze_test.num_explored)
print('Solution')
maze_test.print()

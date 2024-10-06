import random


# Convert direction to movement vector for Kruskal's
lToDir = {"u" : (0,-1), "d" : (0,1), "l" : (-1,0), "r" : (1,0)}


# BINARY TREE
# Complex Techniques - Algorithmic Complexity - Group B


def binaryTree(render, frame, canvas, grid, bias):
    gridCols, gridRows = len(grid), len(grid[0])
    for colCnt, col in enumerate(grid):
        for rowCnt, cell in enumerate(col):
            tempBias = ["d","r"]
            if colCnt == 0 and "l" in bias:
                tempBias.remove("l")
            if colCnt == gridCols-1 and "r" in bias:
                tempBias.remove("r")
            if rowCnt == 0 and "u" in bias:
                tempBias.remove("u")
            if rowCnt == gridRows-1 and "d" in bias:
                tempBias.remove("d")


            if tempBias == bias:
                cell.updateWall(random.choice(tempBias), False)
            elif len(tempBias) == 1:
                cell.updateWall(tempBias[0], False)
            if render:
                cell.render()
                frame.update()
                canvas.pack()


# DEPTH-FIRST GROWTH
# Complex Techniques - Algorithmic Complexity - Group B
# Stack - Group A


def dfg(render, frame, canvas, grid, cell):
    gridCols, gridRows = len(grid), len(grid[0])
    q = [cell]
    # While queue does not contain all elements in grid
    while len(q) != gridCols*gridRows:
        q.append(cell)
        cell.state = 1
        neighbours = cell.getNeighbours(dire=True)
        if len(neighbours[0]) == 0:
            if len(q) != 0:
                # If no neighbours and queue is empty, pop 0th element to set as new cell
                cell = q.pop(0)
        else:
            # Select random neighbour as new cell
            ranIndex = random.randint(0,len(neighbours[0])-1)
            cell.updateWall(neighbours[0][ranIndex], False)
            cell = neighbours[1][ranIndex]
            if render:
                cell.render()
                frame.update()
                canvas.pack()


# RECURSIVE DIVISION
# Complex Techniques - Algorithmic Complexity - Group B
# Recursive Algorithm - Group A


def recursiveDivision(render, frame, canvas, grid, x1, y1, x2, y2, orientation):
    def choose_orientation(width, height):
        if width < height:
            return 0
        elif height < width:
            return 1
        return random.choice([0, 1])


    # Check whether the rectangle is too narrow to divide further
    if y2 - y1 < 1 or x2 - x1 < 1:
        return
    if orientation == 0:
        # Choose a random point between the top and bottom walls of the rectangle
        yWall = random.randint(y1, y2-1)
        # Choose a random opening in the wall
        xPos = random.randint(x1, x2-1)
        # Create a gap in the wall
        for i in range(x1, x2+1):
            if i != xPos:
                grid[i][yWall].updateWall("d", True)
                if render:
                    grid[i][yWall].render()
                    grid[i][yWall+1].render()
        if render:
            frame.update()
            canvas.pack()
        # Recurse on the two sub-rectangles above and below the wall
        recursiveDivision(render, frame, canvas, grid, x1, y1, x2, yWall, choose_orientation(x2-x1, y2-y1))
        recursiveDivision(render, frame, canvas, grid, x1, yWall+1, x2, y2, choose_orientation(x2-x1, y2-yWall-1))
    else:
        # Choose a random point between the left and right walls of the rectangle
        xWall = random.randint(x1, x2-1)
           
        # Choose a random opening in the wall
        yPos = random.randint(y1, y2-1)
        # Create a gap in the wall
        for i in range(y1, y2+1):
            if i != yPos:
                grid[xWall][i].updateWall("r", True)
                if render:
                    grid[xWall][i].render()
                    grid[xWall+1][i].render()
        if render:
            frame.update()
            canvas.pack()
        # Recurse on the two sub-rectangles left and right of the wall
        recursiveDivision(render, frame, canvas, grid, x1, y1, xWall, y2, choose_orientation(x2-x1, y2-y1))
        recursiveDivision(render, frame, canvas, grid, xWall+1, y1, x2, y2, choose_orientation(x2-xWall-1, y2-y1))


# KRUSKAL'S
# Complex Techniques - Algorithmic Complexity - Group B
# OOP (Tree class) - Group A
# Dunder Method (__ior__) for set disjoint-union - Group A
# Tree - Group A


def kruskals(render, frame, canvas, grid):
    gridCols, gridRows = len(grid), len(grid[0])
    class Tree:
        # Constructor
        def __init__(self):
            self.parent = None


        # Find the root of the current tree
        def root(self):
            # If the current tree has a parent, call root() recursively until the root is found and return it
            if self.parent:
                self.parent = self.parent.root()
                return self.parent
            # If the current tree has no parent, return itself as the root
            else:
                return self


        # Check if the current tree is connected to another tree
        def connected(self, other):
            # Compare the roots of the two trees
            return self.root() == other.root()


        # Connect the current tree to another tree
        def connect(self, other):
            # Set the root of the other tree as the parent of the current tree
            other.root().parent = self


        # Combine two trees into a single tree
        def __ior__(self, other):
            self_root, other_root = self.root(), other.root()
            # If the two trees are not already connected, connect them by setting the root of one tree as the parent of the other
            if self_root != other_root:
                self_root.parent = other_root
            return self
       
    edges, sets = [], []
    # Create a grid of Tree objects and add the edges to the list of edges
    for colCnt in range(gridCols):
        treeRow = []
        for rowCnt in range(gridRows):
            # Create a new Tree object for each cell in the grid
            treeRow.append(Tree())
            # Add the top and left edges of each cell to the list of edges
            if rowCnt > 0:
                edges.append([colCnt, rowCnt, "u"])
            if colCnt > 0:
                edges.append([colCnt, rowCnt, "l"])
        sets.append(treeRow)


    random.shuffle(edges)
    for edge in edges:
        x, y, direction = edge
        # Get the coordinates of the neighboring cell in the direction of the current edge
        nx, ny = x + lToDir[direction][0], y + lToDir[direction][1]
        # Get the sets of trees containing the current cell and the neighboring cell
        set1, set2 = sets[x][y], sets[nx][ny]


        # If the two trees are not already connected, connect them and remove the wall between the two cells
        if not set1.connected(set2):
            set1.connect(set2)
            set1 |= set2
            grid[x][y].updateWall(direction, False)


            if render:
                grid[x][y].shade("#ab0", 2)
                frame.update()
                canvas.pack()


# GROWING TREE
# Complex Techniques - Algorithmic Complexity - Group B


def growingTree(render, frame, canvas, cell):
    # Initiate stack with cell already in it; if first cell traversal in the simulation hits a dead end, it will take the other route from the starting cell
    c = [cell]
    while True:
        # Mark cell as visited
        cell.state = 1
        neighbours = cell.getNeighbours(walls=False, dire=True)
        # neighbours[0] = Directions to reach neighbour, neighbours[1] = Neighbours as cell classes
        # If no neighbours exist, pop the stack and set cell as the element. If the stack is empty, the maze has completed
        if len(neighbours[0]) == 0:
            if len(c) != 0:
                cell = c.pop()
            else:
                break
        else:
            # If there is one neighbour, break wall in direction of neighbour, add neighbour to stack and set cell as neighbour
            if len(neighbours[0]) == 1:
                cell.updateWall(neighbours[0][0], False)
                c.append(neighbours[1][0])
                cell = neighbours[1][0]
            else:
                # Otherwise, select a random neighbour
                ranIndex = random.randint(0,len(neighbours[0])-1)
                cell.updateWall(neighbours[0][ranIndex], False)
                c.append(neighbours[1][ranIndex])
                cell = neighbours[1][ranIndex]


            if render:
                cell.shade("#ab0", 2)
                cell.render()
                frame.update()
                canvas.pack()

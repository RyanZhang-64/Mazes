import random, threading, heapq, tkinter, time
from collections import Counter
from queue import PriorityQueue


# TRÉMAUX
# Complex Techniques - Stack (intersection recall) - Group A
# Custom Optimisation - Intersection Recall - Group A
# Algorithmic complexity - Group A


def tremaux(render, frame, canvas, grid, cell, targetCell):
    gridCols, gridRows = len(grid), len(grid[0])
    startCell = cell
    if startCell.rWall: 
        # If cell has rightWall, block off downWall
        direction = [0,-1]
    else:
        # Cell must have one opening, so otherwise block off rightWall
        direction = [-1,0]
    intersectionStack = []
    # intersectionStack takes the tuple form (cell, (simulated direction as if tracer had just backtracked into the intersection))
    while cell != targetCell:
        if render:
            cell.shade("#ab0")
            frame.update()
            canvas.pack()


        neighbours = cell.getNeighbours(walls=True)
        if cell == startCell:
            # If cell is start cell and happens to be an intersection, randomly
            if len(neighbours) == 2:
                direction = random.choice([(1,0),(0,1)])
                if direction == (1,0):
                    intersectionStack.append((cell, (0,-1)))
                else:
                    intersectionStack.append((cell, (-1,0)))
                cell.marks[direction] += 1
                nextNeighbour = grid[cell.col+direction[0]][cell.row+direction[1]]
            else:
                nextNeighbour = neighbours[0]
                direction = (nextNeighbour.col-cell.col, nextNeighbour.row-cell.row)
            cell = nextNeighbour
        elif len(neighbours) == 1: # Dead-end
            if cell == startCell: # If on startCell, treat like straight path
                direction = (neighbours[0].col-cell.col, neighbours[0].row-cell.row)
                cell = neighbours[0]
            else:
                # Otherwise, teleport to previously visited intersection, simulating direction as if you just backtracked into the intersection
                cell, direction = intersectionStack.pop()
                cell.marks[tuple(direction)] += 1
                direction = (-direction[0], -direction[1])
        elif len(neighbours) == 2: # Straight path
            # Move to next cell in path
            neighbours.remove(grid[cell.col-direction[0]][cell.row-direction[1]])
            direction = (neighbours[0].col-cell.col, neighbours[0].row-cell.row)
            cell = neighbours[0]
        elif len(neighbours) > 2: # Intersection
            # Mark incoming wall once
            cell.marks[(-direction[0], -direction[1])] += 1


            # Is intersection visited AND can I go back?
            if cell.intersectionV == True and cell.marks[(-direction[0], -direction[1])] < 2:
                cell, direction = intersectionStack.pop()
                cell.marks[tuple(direction)] += 1
                direction = (-direction[0], -direction[1])
            else:
                cell.intersectionV = True
                # Remove cell I came from and any cells that require passing through a wall of 2 marks
                neighbours.remove(grid[cell.col-direction[0]][cell.row-direction[1]])
                neighbours = [neighbour for neighbour in neighbours if cell.marks[(neighbour.col-cell.col, neighbour.row-cell.row)] < 2]
                if len(neighbours) == 1:
                    # Move to only valid cell
                    nextNeighbour = neighbours[0]
                    direction = [nextNeighbour.col-cell.col, nextNeighbour.row-cell.row]
                else:
                    # What directions can I move that lead to an in-bounds neighbour?
                    possibleDirs = []
                    for x in [(0,-1), (0,1), (-1,0), (1,0)]:
                        if cell.row+x[1] <= gridRows-1 and cell.col+x[0] <= gridCols-1:
                            if grid[cell.col+x[0]][cell.row+x[1]] in neighbours:
                                possibleDirs.append(x)
                    # Counter method returns dictionary of values : occurences in list
                    counts = Counter(cell.marks.values())
                    # Remove direction from dictionary whose key isn't present in possibleDirs
                    dictValues = {k : v for k, v in cell.marks.items() if counts[v] >= 1 and k in possibleDirs}
                    # Only keep occurences of minimum marks
                    directions = [tuple(k) for k, v in dictValues.items() if v == min(dictValues.values())]
                    # If minimum mark occurs more than once in directions
                    # E.g. If counts = {(0,-1) : 0, (0,1) : 0, (-1,0) : 1, (1,0) : 1}, minimum marks = 0
                    # [(0,-1), (0,1)] would be accepted as valid directions
                    if len(directions) > 1: # If duplicate values found in dictionary
                        # Move in random valid direction
                        direction = random.choice(directions)
                    else:
                        # Move in only valid direction
                        direction = directions[0]
                intersectionStack.append((cell, (direction[0], direction[1])))
                nextNeighbour = grid[cell.col+direction[0]][cell.row+direction[1]]
                cell.marks[tuple(direction)] += 1
                cell = nextNeighbour
    # In case last target cell is intersection, mark incoming wall once
    cell.marks[-direction[0], -direction[1]] += 1
    path = []
    while cell != startCell:
        path.append(cell)
        neighbours = cell.getNeighbours(walls=True)
        if cell != grid[gridCols-1][gridRows-1]:
            # Remove cell I came from if I am not on target cell
            neighbours.remove(grid[cell.col-direction[0]][cell.row-direction[1]])
        if len(neighbours) == 1: # Straight path
            # Move to next cell in path
            nextNeighbour = neighbours[0]
            direction = [nextNeighbour.col-cell.col, nextNeighbour.row-cell.row]
        else:
            toPop = []
            # What directions can I move that lead to an in-bounds neighbour?
            for x in cell.marks.keys():
                if cell.row+x[1] > gridRows-1 or cell.col+x[0] > gridCols-1:
                    toPop.append(x)
                elif grid[cell.col+x[0]][cell.row+x[1]] not in neighbours:
                    toPop.append(x)
            for x in toPop:
                cell.marks.pop(x)
            # Follow the wall marked once
            direction = list(cell.marks.keys())[list(cell.marks.values()).index(1)]
            nextNeighbour = grid[cell.col+direction[0]][cell.row+direction[1]]
        cell = nextNeighbour
    for cell in path:
        cell.shade("#fb0")
    grid[0][0].shade("#00FF00")
    targetCell.shade("#FF0000")
    frame.update()
    canvas.pack()


# BREADTH-FIRST SEARCH
# Graph Traversal - Group A


def bfs(render, frame, canvas, grid, startCell, targetCell):
    # Declare a list of frontiers for BFS to process on each iteration of while loop. Start with startCell to start propagation cycle
    frontier = [startCell]
    count = 0
    while targetCell not in frontier and len(frontier) != 0:
        newCells = []
        for cell in frontier:
            cell.state = 1
            cell.distanceFromRoot = count
            newCells += cell.getNeighbours(walls=True)


            if render:
                cell.shade("#ab0")
                frame.update()
                canvas.pack()


        # Remove duplicate elements from newCells
        frontier = list(set(newCells))
        count += 1
    path = []
    cell = targetCell
    while cell != startCell:
        visited = [x for x in cell.getNeighbours(walls=True, visit=False) if x.state == 1]
        distancesFromRoot = [x.distanceFromRoot for x in visited]
        cell = visited[distancesFromRoot.index(min(distancesFromRoot))]
        path.append(cell)
    for cell in path:
        cell.shade("#fb0")
    grid[0][0].shade("#00FF00")
    targetCell.shade("#FF0000")
    frame.update()
    canvas.pack()


# MULTITHREADED BFS
# Complex Techniques - Multithreading - Group A
# Graph Traversal - Group A
# Distributing workload over threads (distribute_cumulative) - Group B
# Simple OOP - Group B


def threadedbfs(render, frame, canvas, grid, startCell, targetCell, threadCount):
    class BFSThread(threading.Thread):
        # Each thread stores list of frontiers and distance from root for all cells in frontier list
        def __init__(self, frontier, count):
            threading.Thread.__init__(self)
            self.frontier = frontier
            self.count = count


        def run(self):
            # newCells records new frontiers to add onto frontiers to be processed for next group of threads
            newCells = []
            for cell in self.frontier:
                cell.state = 1
                cell.distanceFromRoot = self.count
                newCells += cell.getNeighbours(walls=True)
            # Returns list of frontiers without duplicate values, such that program does not have to process same cell twice
            return list(set(newCells))
   
    # Used to distribute frontier cells over a specified number of cells
    # Takes # frontiers and # threads as input
    # Outputs (# threads) slicing pairs of as equal length as possible
    # E.g. frontiers = 8, threadCount = 3, output=[[0,3], [3,6], [6,8]]
    def distribute_cumulative(x, y):
        result = [x // y for i in range(y)]
        remainder = x % y
        for i in range(remainder):
            result[i] += 1
        cumulative_result = [[0, result[0]-1]]
        for i in range(1, y):
            cumulative_result.append([cumulative_result[-1][1] + 1, cumulative_result[-1][1] + result[i]])
        for i in range(y):
            cumulative_result[i][1] += 1
        return cumulative_result
   
    frontier = [startCell]
    count = 0
    while targetCell not in frontier and len(frontier) != 0:
        threads = []
        evenDistribute = distribute_cumulative(len(frontier), threadCount)
        for i in range(len(frontier)):
            # Frontiers designated to thread represented by elements in between list indices evenDistribute[i][0] and evenDistribute[i][1]
            try:
                t = BFSThread(frontier[evenDistribute[i][0]:evenDistribute[i][1]], count)
                t.start()
                threads.append(t)
            except:
                continue


        new_frontier = []
        for t in threads:
            # Prevents thread from being operated on until run() has finished on the thread
            t.join()
            new_frontier += t.run()


        frontier = new_frontier
        count += 1


        if render:
            for x in frontier:
                x.shade("#ab0")
                frame.update()
                canvas.pack()


    path = []
    # Move back from targetCell -> startCell
    cell = targetCell
    while cell != startCell:
        visited = [x for x in cell.getNeighbours(walls=True, visit=False) if x.state == 1]
        distancesFromRoot = [x.distanceFromRoot for x in visited]
        cell = visited[distancesFromRoot.index(min(distancesFromRoot))]
        path.append(cell)
    for cell in path:
        cell.shade("#fb0")
    grid[0][0].shade("#00FF00")
    targetCell.shade("#FF0000")
    frame.update()
    canvas.pack()


# A*
# Complex Techniques - Priority Queue - Group A
# Heuristic Calculation (Manhattan Distance) - Group B
# Graph Traversal - Group A
# Dictionary (aPath) - Group B


def aStar(render, frame, canvas, grid, targetCell, startCell):
    gridCols, gridRows = len(grid), len(grid[0])
    open = []
    # Set distanceFromRoot of targetCell to 0, and set fScore to manhattan distance from startCell (col difference + row difference)
    grid[targetCell[0]][targetCell[1]].distanceFromRoot = 0
    grid[targetCell[0]][targetCell[1]].fScore = abs(targetCell[0]-gridCols-1)+abs(targetCell[1]-gridRows-1)
    heapq.heappush(open, (0, grid[targetCell[0]][targetCell[1]].fScore, targetCell))
    # aPath is a dictionary that maps a cell to its children
    aPath={}
    while open:
        currCell = heapq.heappop(open)[2]
        if currCell == startCell:
            # If cell reaches top-left of grid, start backtracking
            break
        neighbours = grid[currCell[0]][currCell[1]].getNeighbours(walls=True)
        # Calculate g/f score for currCell
        curr_g_score = grid[currCell[0]][currCell[1]].distanceFromRoot+1
        curr_f_score = curr_g_score+abs(currCell[0]-gridCols-1)+abs(currCell[1]-gridRows-1)
        for child in neighbours:
            childCell = (child.col, child.row)
            # If child f score is more than current cell, set g/f score of child to parent's g/f scores
            if curr_f_score < child.fScore:
                child.distanceFromRoot = curr_g_score
                child.fScore = curr_f_score
                heapq.heappush(open, (curr_f_score, abs(childCell[0]-gridCols-1)+abs(childCell[1]-gridRows-1), childCell))
                aPath[childCell] = currCell


                if render:
                    child.shade("#ab0")
                    frame.update()
                    canvas.pack()
   
    fwdPath = {}
    cell = (0,0)
    while cell != targetCell:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
   
    path = [grid[x[0]][x[1]] for x in fwdPath.values()]
    for cell in path:
        cell.shade("#fb0")
    grid[startCell[0]][startCell[1]].shade("#00FF00")
    grid[targetCell[0]][targetCell[1]].shade("#FF0000")
    frame.update()
    canvas.pack()
    
# DIJKSTRA'S
# Complex Techniques - Priority Queue - Group A
# Graph Traversal - Group A


def dijkstras(render, frame, canvas, grid, startCell, targetCell):
    # Initialize start cell distance to 0 and add to the heap
    startCell.distanceFromRoot = 0
    heap = [(startCell.distanceFromRoot, startCell)]


    while len(heap) > 0:
        # Pop cell with smallest distance from heap
        currDist, currCell = heapq.heappop(heap)


        if render:
            currCell.shade("#ab0")
            frame.update()
            canvas.pack()
        # Check if we've reached the end cell
        if currCell == targetCell:
            # Build the path and return it
            path = []
            while currCell.parent:
                path.append(currCell)
                currCell = currCell.parent
            path.append(currCell)
            for cell in path:
                cell.shade("#fb0")
            grid[0][0].shade("#00FF00")
            targetCell.shade("#FF0000")
            frame.update()
            canvas.pack()


        # Update distances to unvisited neighbours
        for neighbour in currCell.getNeighbours(walls=True):
            # Calculate distance from start cell to neighbour
            tentativeDist = currDist + 1
            # If new path to neighbour is shorter, update its distance and parent
            if tentativeDist < neighbour.distanceFromRoot:
                neighbour.distanceFromRoot = tentativeDist
                neighbour.parent = currCell
                # Add to heap to consider as a possible next step
                heapq.heappush(heap, (neighbour.distanceFromRoot, neighbour))


    # If end cell is not reachable from start cell, end
    return


# DEAD-END FILLING
# Complex Techniques - Algorithmic Complexity - Group A


def dead_end_filling(render, frame, canvas, grid, startCell, targetCell):
    path = sum(grid, [])
    deadEnds = []
    for col in grid:
        deadEnds.extend([cell for cell in col if len(cell.getNeighbours(walls=True)) == 1])
    if startCell in deadEnds:
        deadEnds.remove(startCell)
    if targetCell in deadEnds:
        deadEnds.remove(targetCell)
    while len(deadEnds) > 0:
        for cell in deadEnds:
            cell.state = 1
            path.remove(cell)
            neighbour = cell.getNeighbours(walls=True)[0]
            deadEnds.remove(cell)
            if neighbour != targetCell and neighbour != startCell:
                if len(neighbour.getNeighbours(walls=True, visit=True)) == 1:
                    deadEnds.append(neighbour)
            if render:
                cell.shade("#ab0")
        if render:
            frame.update()
            canvas.pack()
    for cell in path:
        cell.shade("#fb0")
    grid[0][0].shade("#00FF00")
    targetCell.shade("#FF0000")
    frame.update()
    canvas.pack()

from queue import PriorityQueue
from classes import Spot
from constants import *


def make_grid(rows, width):
    # to store different spots as grids in the pygame window
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    # draws the grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRIDLINE_COLOR, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GRIDLINE_COLOR, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    # draws the spots stored in grid on the window
    win.fill(BGBASE_COLOR)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    # to get the clicked position ie spot positions from pixel positions
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def h(p1, p2):
    # heuristic functions : using manhattan distances
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def trace_path(came_from, current, start, draw):
    while current in came_from:
        current = came_from[current]  # get the prev node of current
        if current == start:
            break
        current.make_path()
        draw()


def astar(draw, grid, start, end):
    # the astar algorithm to find the path
    # initialization
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # add the start spot to the queue : initialization
    came_from = {}  # what node this node came from, an empty dictionary; newnode : prevnode :: key : value
    g_score = {spot: float("inf") for row in grid for spot in row}  # initializes g_score for each spot as a dictionary
    g_score[start] = 0  # start is also a reference for some spot that is start
    f_score = {spot: float("inf") for row in grid for spot in row}  # similar to above
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    # this is to check if an item is in open_set or not
    # eg. currently start is in the priority queue

    while not open_set.empty():
        # algo runs until the open set is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exit event loops by quitting
                pygame.quit()

        current = open_set.get()[2]  # getting the node from the open_set elements
        # also since this is a priority queue the get() method pops out the lowest f_score element, so current is the
        # element with the lowest f_score present in the queue
        open_set_hash.remove(current)  # also pop from check queue

        if current == end:
            trace_path(came_from, end, start, draw)  # reconstruct path and finish operation when this is over
            end.make_end();
            return True

        for neighbor in current.neighbors:
            neighbor_g_score = 1 + g_score[current]  # path cost is 1 each this is f(x) =  g(x) + h(x)

            if neighbor_g_score < g_score[neighbor]:
                # if the new g-score of neighbor is less than the already written one ,update it
                came_from[neighbor] = current
                g_score[neighbor] = neighbor_g_score
                f_score[neighbor] = neighbor_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    # add the neighbor in the open-set and its hash if its not there
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # color it as open
                    draw()  # draw the current frame ie all the spots

        if current != start:
            # if this is not a start node then make it close
            # will be drawn as closed in the next iteration
            current.make_closed()

    return False  # ie when the current == True doesn't work ie there is no path

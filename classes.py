from constants import *
import pygame


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = WIDTH
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.color = BGBASE_COLOR

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == VISITEDNODE_COLOR

    def is_open(self):
        return self.color == SEENNODE_COLOR

    def is_barrier(self):
        return self.color == WALL_COLOR

    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == END_COLOR

    def reset(self):
        self.color = BGBASE_COLOR

    def make_closed(self):
        self.color = VISITEDNODE_COLOR

    def make_open(self):
        self.color = SEENNODE_COLOR

    def make_barrier(self):
        self.color = WALL_COLOR

    def make_end(self):
        self.color = END_COLOR

    def make_path(self):
        self.color = FINALPATH_COLOR

    def make_start(self):
        self.color = START_COLOR

    def draw(self, win):
        """
        draw a rectangle at position x and y of dimension [width ,width]
        :param win: The window to draw stuff at
        :return: draws stuff at window win
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            # if down spot a barrier or not, if it isn't append it
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            # if up spot a barrier or not, if not append
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            # if right spot is not a barrier append it
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            # if left spot is not a barrier append it
            self.neighbors.append(grid[self.row][self.col - 1])

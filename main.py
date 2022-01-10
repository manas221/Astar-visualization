import pygame
from maze import *
from functions import *
from constants import *

start = None  # the 'start' spot
end = None  # the 'end' spot

run = True
started = False

grid = make_grid(ROWS, WIDTH)

while run:
    draw(WIN, grid, ROWS, WIDTH)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if started:
            continue

        if pygame.mouse.get_pressed()[0]:
            # events when Left button is pressed
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_position(pos, ROWS, WIDTH)
            spot = grid[row][col]

            if start is None:
                # if start has none type ie it is not initialized
                start = spot
                start.make_start()

            elif end is None and spot != start:
                # if end has none type ie it is not initialized
                end = spot
                end.make_end()

            elif spot != end and spot != start:
                # spot is neither end nor start so it must be a barrier now
                spot.make_barrier()

        elif pygame.mouse.get_pressed()[2]:
            # events when the right mouse button is pressed
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_position(pos, ROWS, WIDTH)
            spot = grid[row][col]
            spot.reset()
            # clear the spot when right button is pressed

            # since the end button would be reset before the start
            # reset end to None ,and later equate it to start
            if spot == start:
                start = end
            elif spot == end:
                end = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start is not None and end is not None:
                for row in grid:
                    for spot in row:
                        spot.update_neighbors(grid)  # explicitly calling to update the neighbor info in grid
                x = lambda: draw(WIN, grid, ROWS, WIDTH)
                astar(x, grid, start, end)

            if event.key == pygame.K_c:
                # reset the board
                start = None
                end = None
                grid = make_grid(ROWS, WIDTH)

            if event.key == pygame.K_b:
                addmaze(grid)
                # draw_on_grid(grid ,ROWS)

pygame.quit()

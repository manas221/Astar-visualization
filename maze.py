import numpy as np


def choose_orientation(width, height):
    # 0 means width ,draw wall parallel to width
    # 1 means height ,draw wall parallel to height
    if width < height:
        return 0
    elif width > height:
        return 1
    else:
        return np.random.choice([0, 1])


def rmaze(map):
    height = map.shape[0]
    width = map.shape[1]
    if height < 2 or width < 2:
        return
    vertical = choose_orientation(width, height)
    passage_index = wall_index = 0
    if vertical:
        # vertical wall
        if width < 1:
            return
        wall_index = np.random.randint(0, width - 1)
        map[:, wall_index] = 1
        passage_index = np.random.randint(0, height - 1)
        map[passage_index, wall_index] = 0

        # # recurse on 4 subgrid
        # TL = map[0:passage_index,0:wall_index]
        # TR = map[0:passage_index,wall_index+1:-1]
        # PL = map[passage_index ,0:wall_index]
        # BL = map[passage_index+1:-1,0:wall_index]
        # BR = map[passage_index+1:-1,wall_index+1:-1]
        # PR = map[passage_index ,wall_index+1:-1]
        # rmaze(TL)
        # rmaze(TR)
        # rmaze(PL)
        # rmaze(BL)
        # rmaze(BR)
        # rmaze(PR)
        Left = map[:, 0:wall_index - 1]
        Right = map[:, wall_index + 2:-1]
        rmaze(Left)
        rmaze(Right)

    else:
        # horizontal wall
        if height < 1:
            return
        wall_index = np.random.randint(0, height - 1)
        map[wall_index, :] = 1
        passage_index = np.random.randint(0, width - 1)
        map[wall_index, passage_index] = 0

        # # recurse on 4 subgrids
        # TL = map[0:wall_index ,0:passage_index]
        # TR = map[0:wall_index ,passage_index+1:-1]
        # PT = map[0:wall_index ,passage_index]
        # BL = map[wall_index+1:-1 ,0:passage_index]
        # BR = map[wall_index+1:-1, passage_index+1:-1]
        # PB = map[wall_index+1:-1 ,passage_index]
        # rmaze(TL)
        # rmaze(TR)
        # rmaze(PT)
        # rmaze(BL)
        # rmaze(BR)
        # rmaze(PB)
        Top = map[0:wall_index - 1, :]
        Bottom = map[wall_index + 2:-1, :]
        rmaze(Top)
        rmaze(Bottom)


def addmaze(grid):
    # generating numpy array for the grid
    map = np.zeros([len(grid), len(grid[0])], dtype=bool)

    # now generate maze recursively on map
    rmaze(map)

    # tracing map on grid
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if map[i][j]:
                grid[j][i].make_barrier()
            else:
                grid[j][i].reset()

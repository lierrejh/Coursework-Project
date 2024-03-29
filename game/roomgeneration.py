import csv, os, random
from typing import List, Tuple


# Write up:
# Write about Room gen process and issues/figuring out what I should do
# Easier when spoken about but harder when actually doing
# Breaking down into steps makes it easier to do 
# Write about path finding for hallways and issues / figuring it out
# Write about methods of aglorithms (BSP, Cellular automata etc and why I ended up with this one)
# This works because cellular automata gives badly shaped rooms for this game tyoe
# BSP is inefficient and cannot be implemented without even more inefficiencies 
# (because of how the map is created)
# This is good but issues lie within the fact that some rooms may be more clustered together but gives
# a (hopefully) good feel in game 
# Potentially talk about struggles of implementation and other ways I could have done the map system
# Pygame is not an easy engine as solutions require a solo approach and not the best for games like this
# Other engines that could have worked but pygame made me think more about what I was doing with no help
# Issues with implementing boss room (special sizing) etc
# Tried using algo but took too long (too slow time eff)
# What about having a list and taking all values from the list leaving you with one left


# Creates a new CSV (for map) if not already one otherwise replaces the old one
def create_blank_CSV():
    try:
        with open('assets/map/MapTest2.csv', 'x', newline = '') as file:
            a = csv.writer(file,delimiter=',')
            row = []
            # Sets all values to -1 which is dark
            for i in range(1,131):
                row.append('-1')
            
            for j in range(1,71):
                a.writerow(row)
    except:
        os.remove("assets/map/MapTest2.csv")
        create_blank_CSV()

# Sets the tiles which border nothing to be walls
def border_tiles(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        border_tiles = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] == '50':
                    if i > 0 and data[i-1][j] == '-1':
                        border_tiles.append((i, j))
                    if i < len(data) - 1 and data[i+1][j] == '-1':
                        border_tiles.append((i, j))
                    if j > 0 and data[i][j-1] == '-1':
                        border_tiles.append((i, j))
                    if j < len(data[0]) - 1 and data[i][j+1] == '-1':
                        border_tiles.append([i, j])
        return border_tiles

# Expands the central points of rooms by a given value in order to create the actual room
def room_expansion(points):
    tiles = []
    # Iterate through the points
    for point in points:
        x, y = point
        # Iterate through the tiles in a 10 by 10 radius
        for i in range(x-6, x+7):
            for j in range(y-6, y+7):
                tile = (i, j)
                # Append the tile to the list if it is not already in the list
                if tile not in tiles:
                    tiles.append(list(tile))
    return tiles

# Updates the CSV with the tiles generated
def update_CSV(tiles, tile_type):
    a = csv.reader(open('assets/map/MapTest2.csv'))
    lines = list(a)
    for i in tiles:
        ROW_NUM = i[0]
        COL_NUM = i[1]
        if tile_type == 'Floor':
            lines[ROW_NUM][COL_NUM] = '50'
        elif tile_type == 'Wall':
            lines[ROW_NUM][COL_NUM] = '16'
        writer = csv.writer(open('assets/map/MapTest2.csv', 'w'))
        writer.writerows(lines)

# Generates the central points of the rooms
def central_points_generation():
    create_blank_CSV()
    room_center_points = []
    # Generating typical rooms within generation
    # Cannot use for loop, must be while -> Needs cases where it does or does not increase
    THRESHOLD_DISTANCE = 16
    MAX_ROOMS = 7
    too_close = False

    while len(room_center_points) < MAX_ROOMS:
        # Generate random room_center_points
        cols = random.randint(25, 75)
        rows = random.randint(12, 50)
        point = (rows, cols)

        # Check if the point is too close to any existing point
        too_close = False
        for existing_point in room_center_points:
            distance = ((existing_point[0] - point[0]) ** 2 + (existing_point[1] - point[1]) ** 2) ** 0.5
            if distance < THRESHOLD_DISTANCE:
                too_close = True
                break

        # If the point is not too close, add it to the list
        if not too_close:
            room_center_points.append(list(point))
    return room_center_points

# Typing allows for better understanding of what is going on and what is being returned
# Removes overlapping points in order to prevent rooms and oto many paths from being 
# generated on top of each other
def remove_overlapping_points(path: List[List[int]]) -> List[List[int]]:
    unique_points = []
    for point in path:
        if point not in unique_points:
            unique_points.append(point)
    return unique_points

# Creates a path from a list of points using Bresenham's line algorithm
def create_path(points: List[List[int]]) -> List[Tuple[int, int]]:
    points = [tuple(point) for point in points]
    path = [list(points[0])]
    for i in range(len(points) - 1):
        path += bresenham(points[i], points[i + 1])
    return path

# Bresenham's line algorithm
def bresenham(p1: Tuple[int, int], p2: Tuple[int, int]) -> List[Tuple[int, int]]:
    # Start and end points
    x1, y1 = p1
    x2, y2 = p2
    # List of points on the path is declared
    path = []
    # Absolute value of the difference between the start and end points
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    
    # Variables are set to -1 or 1 depending on whether the line is moving left or right, 
    # and up or down respectively.
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    
    # If the line is moving more horizontally than vertically
    if dx > dy:
        # The error is set to half the difference between the start and end points
        err = dx / 2.0
        # While the line has not reached the end point
        while x != x2:
            path.append([x, y])
            err -= dy
            # If the error is less than 0, the line moves up or down depending on the value of sy
            if err < 0:
                y += sy
                err += dx
            x += sx
    
    else:
        err = dy / 2.0
        while y != y2:
            path.append([x, y])
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    path.append([x, y])
    return path

# Expands the path by a given radius in order to create a larger path
def expand_path(path: List[Tuple[int, int]], radius: int) -> List[Tuple[int, int]]:
    expanded_path = []
    for point in path:
        x, y = point[0], point[1]
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                expanded_path.append([i, j])
    return expanded_path

# Comverts the points to the map scale
def get_converted_points(points):
    converted_points = []
    for i in points:
        x = i[0] * 40
        y = i[1] * 39
        converted_points.append([x, y])
    return converted_points

# Generates the rooms and paths and gives them to tiles required and updates the CSV
def room_generation():
    FLOOR = 'Floor'
    WALL = 'Wall'
    
    room_center_points = central_points_generation()
    expanded_room = room_expansion(room_center_points)

    path = remove_overlapping_points(create_path(room_center_points))

    # Update the CSV
    update_CSV(expand_path(path, 2), FLOOR)
    update_CSV(expanded_room, FLOOR)
    update_CSV(border_tiles('assets/map/MapTest2.csv'), WALL)
    
    # Return converted points to map scale
    return get_converted_points(room_center_points)
    
# Generates the spawn points for the player
def get_player_spawn(points):
        random_spawn_index = random.randint(0,len(points) -1)
        return points[random_spawn_index]

    

import csv, os, random
from collections import defaultdict

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
            for i in range(1,151):
                row.append('-1')
            
            for j in range(1,151):
                a.writerow(row)
    except:
        os.remove("assets/map/MapTest2.csv")
        create_blank_CSV()

# Room generation algorithm
    #BSP?
    #Place room centers, scan list to find room centers and then expand by a range (to make room larger)
    #Save location of room centers
    #Djikstra's in between rooms centers to make paths


def room_expansion(points):
    tiles = []
    # Iterate through the points
    for point in points:
        x, y = point
        # Iterate through the tiles in a 10 by 10 radius
        for i in range(x-8, x+9):
            for j in range(y-8, y+9):
                tile = (i, j)
                # Append the tile to the list if it is not already in the list
                if tile not in tiles:
                    tiles.append(list(tile))
    return tiles

def update_CSV(tiles):
    a = csv.reader(open('assets/map/MapTest2.csv'))
    lines = list(a)
    for i in tiles:
        ROW_NUM = i[0]
        COL_NUM = i[1]
        lines[ROW_NUM][COL_NUM] = '50'
        writer = csv.writer(open('assets/map/MapTest2.csv', 'w'))
        writer.writerows(lines)


def central_points_generation():
    create_blank_CSV()
    room_center_points = []
    # Generating typical rooms within generation
    # Cannot use for loop, must be while -> Needs cases where it does or does not increase
    THRESHOLD_DISTANCE = 20
    MAX_ROOMS = 9
    too_close = False

    while len(room_center_points) < MAX_ROOMS:
        # Generate random room_center_points
        cols = random.randint(10, 90)
        rows = random.randint(10, 90)
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

        # # Create a dictionary to store the graph
        # graph = defaultdict(list)

        # # Create a path between the room_center_points using Dijkstra's algorithm
        # for i in range(len(room_center_points)):
        #     for j in range(i+1, len(room_center_points)):
        #         distance = ((room_center_points[i][0] - room_center_points[j][0]) ** 2 + (room_center_points[i][1] - room_center_points[j][1]) ** 2) ** 0.5
        #         graph[i].append((j, distance))
        #         graph[j].append((i, distance))

    return room_center_points

def room_generation():
    room_center_points = central_points_generation()
    full_room = room_expansion(room_center_points)
    update_CSV(full_room)

room_generation()
import csv, os, random
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
            for i in range(1,81):
                row.append('-1')
            
            for j in range(1,101):
                a.writerow(row)
    except:
        os.remove("assets/map/MapTest2.csv")
        create_blank_CSV()

# Room generation algorithm
def generate_room_positions(room_center_points, i):
    # a = csv.reader(open('assets/map/MapTest2.csv'))
    # lines = list(a)
    # lines[2][1] = '20'
    # writer = csv.writer(open('assets/map/MapTest2.csv', 'w'))
    # writer.writerows(lines)

    #BSP?
    #Place room centers, scan list to find room centers and then expand by a range (to make room larger)
    #Save location of room centers
    #Djikstra's in between rooms centers to make paths
    
    points = []
    points.append(random.randint(10,70))
    points.append(random.randint(10,90))

def check_room_locations(coords, i):
    pass

    


def room_generation():
    create_blank_CSV()
    room_center_points = []
    # Generating typical rooms within generation
    # Cannot use for loop, must be while -> Needs cases where it does or does not increase
    THRESHHOLD_DISTANCE = 10
    MAX_ROOMS = 9
    too_close = False

    while len(room_center_points) < MAX_ROOMS:
        # Only on first iteration will it be added to the list
        # print(i)
        if i == 0:    
            room_center_points.append(generate_room_positions(room_center_points))
            # print(room_center_points)
            i += 1
        # Otherwise check against other room positions to make sure not too close    
        else:
            new_points = generate_room_positions(room_center_points, i)
            # print(new_points)
            for k in room_center_points:
                if ((new_points[0] <= k[0] + 10) and (new_points[1] <= k[1] + 10))  or ((new_points[0] == k[0] - 10) and (new_points[1] == k[1] - 10)):
                    checks += 1 
                    print(checks)
            if checks == 9:
                room_center_points.append(new_points)
                i +=1 
    
    print(room_center_points)
    a = csv.reader(open('assets/map/MapTest2.csv'))
    lines = list(a)
    for i in room_center_points:
        ROW_NUM = i[0]
        COL_NUM = i[1]
        lines[COL_NUM][ROW_NUM] = '50'
        writer = csv.writer(open('assets/map/MapTest2.csv', 'w'))
        writer.writerows(lines)


    
    # list = [[1,3], [2,4]]
    # print(list[1][0])
    # Multi-dimensional lists will be very useful!

room_generation()

""" Write a function for implementing path generation between points in the map"""
# Path generation algorithm
def room_generation():
    Generate random points
    Check if points are too close to eachother
    If not then add to list
    If so then generate new points
    Once 9 points are generated then create a path between them
    Use Djikstra's algorithm to create path between points
    Save path in CSV file
    Use the CSV file to create the map 
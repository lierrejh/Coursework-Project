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
def generate_room_positions():
    # a = csv.reader(open('assets/map/MapTest2.csv'))
    # lines = list(a)
    # lines[2][1] = '20'
    # writer = csv.writer(open('assets/map/MapTest2.csv', 'w'))
    # writer.writerows(lines)

    #BSP?
    #Place room centers, scan list to find room centers and then expand by a range (to make room larger)
    #Save location of room centers
    #Djikstra's in between rooms centers to make paths

    rand_cols = random.randint(7, 91)
    rand_rows = random.randint(4, 75)
    return rand_rows, rand_cols

def check_room_locations(coords, i):
    pass

    


def room_generation():
    create_blank_CSV()
    list = [[1,3], [2,4]]
    print(list[1][0])
    # Multi-dimensional lists will be very useful!

room_generation()
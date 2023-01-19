import csv, os

def delete_current_file():
    os.remove("MapTest3.csv")

def create_CSV():
    with open('game/MapTest2.csv', 'w', newline = '') as file:
        a = csv.writer(file,delimiter=',')
        cols = [i for i in]
import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
import time
import keyboard
import math
import random

#F for starting the bot
#G for pausing it (if the automatic pause doesn't reset the board)
#X finishes the program

#Minesweeper coordinates MAKE SURE TO CHANGE IT TO YOUR CONFIGURATION
mon = {'left': 801, 'top': 250, 'width': 600, 'height': 500}

#variables later used
vai = 0
firstTime = False
clicked = False

#grid list to store tile values
rows, cols = (20, 24)
backupGrid = grid = [[0 for i in range(cols)] for j in range(rows)]


#getting all stock tile pixel colors, it is the x=13 y=11 of each tile
blank = (159, 194, 229)
blank2 = (153, 184, 215)
green = (81, 215, 170)
green2 = (73, 209, 162)
num1 = (206, 124, 43)
num2 = (76, 150, 84)
num3 = (46, 46, 212)
num4 = (162, 50, 138)
num5 = (1, 144, 253)
num6 = (165, 153, 0)

stockTiles = [blank, blank2, green, green2, num1, num2, num3, num4, num5, num6]

#check if a color matches
def colorNear(a, b):
    for i in range(3):
        
        if abs(a[i] - b[i]) > 30: test = False
        else: test = True

        if test == False: return False
    return True



#identifiyng which tile it is based in stockTiles
def getTile(input):

    stockIdx = 100

    for i,base in enumerate(stockTiles):
        if colorNear(base, input): 
            stockIdx = i
    
    switcher = {
        0: "blank",
        1: "blank",
        2: "green",
        3: "green",
        4: "num1",
        5: "num2",
        6: "num3",
        7: "num4",
        8: "num5",
        9: "num6",
    }
    return switcher.get(stockIdx, "nothing")

#getting valid position
def isValidPos(i, j, n, m):
 
    if (i < 0 or j < 0 or i > n - 1 or j > m - 1):
        return 0
    return 1
 
 
# Function that returns all adjacent elements
def getAdjacent(arr, i, j):
 
    # Size of given 2d array
    n = len(arr)
    m = len(arr[0])
 
    # Initialising a vector array
    # where adjacent element will be stored
    v = []
 
    # Checking for all the possible adjacent positions
    if (isValidPos(i - 1, j - 1, n, m)):
        v.append(arr[i - 1][j - 1])
    else:
         v.append("nothing")
    if (isValidPos(i - 1, j, n, m)):
        v.append(arr[i - 1][j])
    else:
         v.append("nothing")
    if (isValidPos(i - 1, j + 1, n, m)):
        v.append(arr[i - 1][j + 1])
    else:
         v.append("nothing")
    if (isValidPos(i, j - 1, n, m)):
        v.append(arr[i][j - 1])
    else:
         v.append("nothing")
    if (isValidPos(i, j + 1, n, m)):
        v.append(arr[i][j + 1])
    else:
         v.append("nothing")
    if (isValidPos(i + 1, j - 1, n, m)):
        v.append(arr[i + 1][j - 1])
    else:
         v.append("nothing")
    if (isValidPos(i + 1, j, n, m)):
        v.append(arr[i + 1][j])
    else:
         v.append("nothing")
    if (isValidPos(i + 1, j + 1, n, m)):
        v.append(arr[i + 1][j + 1])
    else:
         v.append("nothing")
 
    # Returning the vector
    return v


#clicking adjacent tiles based on logic and tile value
def clickAdjacent(indices, gridCoords, click):
    switcherCoords = {
        0: [-1, -1],
        1: [0, -1],
        2: [1, -1],
        3: [-1, 0],
        4: [1, 0],
        5: [-1, 1],
        6: [0, 1],
        7: [1, 1],
    }

    coords = [gridCoords[0]*25+805, gridCoords[1]*25+255] #adds monitor left and right paddings, plus 12 and multiplies by tile resolution, 25x25

    for i in indices:
        adjacentTiles = switcherCoords.get(i, "nothing")

        relCoords = [i * 25 for i in adjacentTiles]

        if click == 'right':
            grid[gridCoords[1]+adjacentTiles[1]][gridCoords[0]+adjacentTiles[0]] = "flag"
        else:
            grid[gridCoords[1]+adjacentTiles[1]][gridCoords[0]+adjacentTiles[0]] = "blank"
            pyautogui.click(coords[0]+relCoords[0], coords[1]+relCoords[1], button=click)



#Sees the board and applies basic minesweeper logic to it, calling click function
def processImg(img):
    for i in range(20):
        for j in range(24):
            iC = i*25
            jC = j*25
            croppedPixel = img[iC+11, jC+13] #alling to specif pixel of a tile
            if grid[i][j] != "flag" and grid[i][j] != "used":
                grid[i][j] = getTile(croppedPixel)

    clicked = False

    for i in range(20):
        for j in range(24):
            if sum(row.count("nothing") for row in grid) >= 50:return 2,clicked
            tile = grid[i][j]
            if tile.startswith("num"):
                adjacent = getAdjacent(grid, i, j)
                gridCoords = [j, i]
                num = int(tile[-1:])
                numGreen = adjacent.count("green")
                numFlag = adjacent.count("flag")

                if num - numFlag == numGreen and numGreen != 0:
                    indices = [i for i, x in enumerate(adjacent) if x == "green"]
                    clickAdjacent(indices, gridCoords, 'right')
                    vai = 1
                    clicked = True
                    grid[i][j] = "used"

                elif num - numFlag == 0 and numGreen != 0:
                    indices = [i for i, x in enumerate(adjacent) if x == "green"]
                    clickAdjacent(indices, gridCoords, 'left')
                    vai = 1
                    clicked = True
                    grid[i][j] = "used"


    return 1,clicked
        

#Get the indexes of a specifi element in a 2D List
def indexList_2d(myList, v):
    indices = []
    for idxI, i in enumerate(myList):
        if i.count(v) != 0:
            for idxJ, i in enumerate(myList[idxI]):
                if i == v:
                    indices.append((idxI, idxJ))
    return indices


#Loop that identifies key presses to stop and resume and get monitor image
with mss() as sct:
    while True:


        #starts the program        
        if keyboard.is_pressed('f'):  
            vai = 1
            print("start")
            firstTime = True


        #Pauses the program
        if keyboard.is_pressed('g') or vai == 2: 
            vai = 0
            print("paused")
            grid = [[0 for i in range(24)] for j in range(20)]
            firstTime = False
            pyautogui.click(1000, 580)


        #finishes the program
        if keyboard.is_pressed('x'):  
            print("finished")
            #print('\n'.join([' '.join(['{:4}'.format(item) for item in row]) for row in grid]))
            break

        
        #clicks 3 spots at the start of the game CHANGE ITS COORDINATES IF YOU WANT TO REPLICATE ON YOUR MACHINE
        if firstTime:
            pyautogui.click(1116, 486)
            #pyautogui.click(912, 359)
            #pyautogui.click(1265, 364)
    

        if vai == 1:
            pyautogui.moveTo(795,230)

            #getting the screenshot as an image
            screenShot = sct.grab(mon)
            img = np.array(screenShot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            vai, clicked = processImg(img)



        if firstTime:
            firstTime = False
            clicked = True


        #clicks a random green tile when its logic isn't sufficient
        if clicked == False and vai == 1 and firstTime == False:
            try:
                i,j = random.choice(indexList_2d(grid, "green"))
                pyautogui.click(j*25+805, i*25+255)
                print("clicked random")
            except:
                print("Finished the Minesweeper")
                vai = 0
                grid = [[0 for i in range(24)] for j in range(20)]
                firstTime = False
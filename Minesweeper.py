import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
import keyboard
import math
import random
import mouse

#F for starting the bot
#G for pausing it (if the automatic pause doesn't reset the board)
#X finishes the program

#Minesweeper coordinates specific for monitor config
width = 600
height = 500
leftMargin = 801
topMargin = 250
tileSide = 25
tileHalf = 12
specificPixelI = 11
specificPixelJ = 13

mon = {'left': leftMargin, 'top': topMargin, 'width': width, 'height': height}

#variables later used
vai = 0
firstTime = False
clicked = False
frames = 0

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

#clicking function
def click_mouse(x, y, button):
    mouse.move(x, y, absolute=True)
    mouse.click(button=button)


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

    coords = [gridCoords[0]*tileSide+leftMargin+tileHalf, gridCoords[1]*tileSide+topMargin+tileHalf] #adds monitor left and right margins, plus half of a tile and multiplies by tile resolution

    for i in indices:
        adjacentTiles = switcherCoords.get(i, "nothing")

        relCoords = [i * tileSide for i in adjacentTiles]

        if click == 'right':
            grid[gridCoords[1]+adjacentTiles[1]][gridCoords[0]+adjacentTiles[0]] = "flag"
            #click_mouse(coords[0]+relCoords[0], coords[1]+relCoords[1], click)
            #print("flag", gridCoords[1]+adjacentTiles[1],gridCoords[0]+adjacentTiles[0])
        else:
            grid[gridCoords[1]+adjacentTiles[1]][gridCoords[0]+adjacentTiles[0]] = "blank"
            click_mouse(coords[0]+relCoords[0], coords[1]+relCoords[1], click)
            #print("clicked", gridCoords[1]+adjacentTiles[1],gridCoords[0]+adjacentTiles[0])


#Sees the board and applies basic minesweeper logic to it, calling click function
def processImg(img):
    for i in range(20):
        for j in range(24):
            iC = i*25
            jC = j*25
            croppedPixel = img[iC+specificPixelI, jC+specificPixelJ] #alling to specif pixel of a tile
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
                
                if num == numFlag:
                    grid[i][j] = "used"

                if num - numFlag == numGreen and numGreen != 0:
                    indices = [i for i, x in enumerate(adjacent) if x == "green"]
                    clickAdjacent(indices, gridCoords, 'right')
                    vai = 1
                    clicked = True
                    grid[i][j] = "used"

                if num - numFlag == 0 and numGreen != 0:
                    indices = [i for i, x in enumerate(adjacent) if x == "green"]
                    clickAdjacent(indices, gridCoords, 'left')
                    vai = 1
                    clicked = True
                    grid[i][j] = "used"


    return 1,clicked




#applies logic with 2 tiles at a time
def processAdv(img):

    for i in range(20):
        for j in range(24):
            iC = i*25
            jC = j*25
            croppedPixel = img[iC+specificPixelI, jC+specificPixelJ] #alling to specif pixel of a tile
            if grid[i][j] != "flag" and grid[i][j] != "used":
                grid[i][j] = getTile(croppedPixel)


    possibleBombsComplete = []
    numbers = []

    switcherCoords = {
        0: [-1, -1],
        1: [-1, 0],
        2: [-1, 1],
        3: [0, -1],
        4: [0, 1],
        5: [1, -1],
        6: [1, 0],
        7: [1, 1],
    }

    for i in range(20):
        for j in range(24):
            tile = grid[i][j]
            possibleBombs = []

            if tile.startswith("num"):
                adjacent = getAdjacent(grid, i, j)
                num = int(tile[-1:])
                numFlag = adjacent.count("flag")


                indices = [i for i, x in enumerate(adjacent) if x == "green"]
                

                for relative in indices:
                    relativeCoords = switcherCoords.get(relative, "nothing")
                    possibleBombs.append([i+relativeCoords[0],j+relativeCoords[1]])
                    
                possibleBombsComplete.append(possibleBombs)
                numbers.append(num-numFlag)

    
    for iBomb in range(len(possibleBombsComplete)):
        for iBomb2 in range(iBomb+1,len(possibleBombsComplete)):
            first = possibleBombsComplete[iBomb]
            second = possibleBombsComplete[iBomb2]

            sub = False

            if(all(x in first for x in second)):

                diff = [lst for lst in first if lst not in second]
                one = first
                two = second

                iOne = iBomb
                iTwo = iBomb2
                sub = True

            elif(all(x in second for x in first)):
                diff = [lst for lst in second if lst not in first]
                one = second
                two = first

                iOne = iBomb2
                iTwo = iBomb
                sub = True


            if sub:
                if len(diff) > 0:
                    vai = 1
                    clicked = True

                    #print("diff",diff)

                    if numbers[iBomb] == numbers[iBomb2]:

                        for d in diff:
                            grid[d[0]][d[1]] = "blank"
                            click_mouse(d[1]*tileSide+leftMargin+tileHalf, d[0]*tileSide+topMargin+tileHalf, "left")
                            #print("clicked adv", d[0],d[1])
                            
                    elif numbers[iBomb] - numbers[iBomb2] == len(diff):
                        for d in diff:
                            grid[d[0]][d[1]] = "flag"
                            #click_mouse(d[1]*tileSide+leftMargin+tileHalf, d[0]*tileSide+topMargin+tileHalf, "right")
                            #print("flag adv", d[0],d[1])

            
    
    return 1





#Get the indexes of a specific element in a 2D List
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
            mouse.move(1000, 580, absolute=True)


        #finishes the program
        if keyboard.is_pressed('x'):  
            print("finished")
            #print('\n'.join([' '.join(['{:4}'.format(item) for item in row]) for row in grid]))
            break

        
        #clicks 3 spots at the start of the game
        if firstTime:
            click_mouse(1116, 520, "left")
            #click_mouse(912, 359, "left")
            #click_mouse(1265, 364, "left")
            clicked = True
            
    

        if vai == 1:
            mouse.move(795,230, absolute=True)

            #getting the screenshot as an image
            screenShot = sct.grab(mon)
            img = np.array(screenShot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            vai, clicked = processImg(img)
            processAdv(img)


        if clicked:
            frames = 0


        #clicks a random green tile when its logic isn't sufficient (8 frames without clicking)
        if clicked == False and vai == 1 and firstTime == False:

            if frames >= 8:
                try:
                    i,j = random.choice(indexList_2d(grid, "green"))
                    click_mouse(j*tileSide+leftMargin+tileHalf, i*tileSide+topMargin+tileHalf,"left")
                    clicked = True
                    frames = 0
                    print("clicked random")
                except:
                    print("Finished the Minesweeper")
                    vai = 0
                    grid = [[0 for i in range(24)] for j in range(20)]
                    firstTime = False

            frames+=1


        firstTime = False

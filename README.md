# Minesweeper Bot
 Python Minesweeper Bot that uses openCV
 
 It detects a certain area of your screen, the corresponding area of a google minesweeper on hard difficulty, only the 24x20 grid.
 If you want to use this on your computer, make sure to change all values regarding to resolution and margins
 
 F to start
 G to pause
 X to exit
 
 Sometimes it will either fail when its logic isn't sufficient and it goes for luck by clicking a random green spot and analysing the board.
 Its logic consists in analyzing all number tiles and checking if any flags can be placed around or if any of the 8 surrouding tiles can be clicked. Then it analyzes 2 number tiles at a time to check for "co-surrounding" tiles to click or flag the exclusive ones.

Youtube video demonstrating the application: https://www.youtube.com/watch?v=axMwU9gabRE

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     for fun :)
#
# Author:      ROHIT
#
# Created:     01/04/2014
# Copyright:   (c) ROHIT 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!C:/Python27/python.exe

from Tkinter import *
import tkMessageBox, random

def mousePressed(event):
    canvas = event.widget.canvas
    snakeBoard = canvas.data["snakeBoard"]
    moveSnake(canvas)

def keyPressed(event):
    canvas = event.widget.canvas
    if (event.keysym == "Up"):
        canvas.data["previous_posx"] = -1
        canvas.data["previous_posy"] = 0
    elif (event.keysym == "Down"):
        canvas.data["previous_posx"] = 1
        canvas.data["previous_posy"] = 0
    elif (event.keysym == "Left"):
        canvas.data["previous_posx"] = 0
        canvas.data["previous_posy"] = -1
    elif (event.keysym == "Right"):
        canvas.data["previous_posx"] = 0
        canvas.data["previous_posy"] = 1

def moveSnake(canvas):
    x = canvas.data["previous_posx"]
    y = canvas.data["previous_posy"]
    snakeBoard = canvas.data["snakeBoard"]
    i = 0
    for i in range(0, canvas.data["len"]):
        searchElement(canvas, i + 1)
        if(i == 0):
            canvas.data["snake_tailx"] = canvas.data["curcol"]
            canvas.data["snake_taily"] = canvas.data["currow"]
        snakeBoard[canvas.data["curcol"]][canvas.data["currow"]] = i

#    if( (canvas.data["curcol"] + x ) < len(snakeBoard[0]) and (canvas.data["currow"] + y) < len(snakeBoard)):
#        if((canvas.data["curcol"] + x ) >=0 and (canvas.data["currow"] + y) >= 0):
    snakeBoard[(canvas.data["curcol"] + x) % 10][(canvas.data["currow"] + y) % 10] = canvas.data["len"]
    if(canvas.data["snake_tailx"] == canvas.data["food_posx"] and canvas.data["snake_taily"] == canvas.data["food_posy"]):
        increaseLenght(canvas)
    canvas.data["snakeBoard"] = snakeBoard

def searchElement(canvas, val):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if(snakeBoard[col][row] == val):
                canvas.data["currow"] = row
                canvas.data["curcol"] = col

def increaseLenght(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if(snakeBoard[row][col] > 0):
                snakeBoard[row][col] += 1
    snakeBoard[canvas.data["snake_tailx"]][canvas.data["snake_taily"]] = 1
    canvas.data["snakeBoard"] = snakeBoard
    canvas.data["len"] += 1
    canvas.data["food_posx"] = -1
    canvas.data["food_posy"] = -1
    generateFood(canvas)


def checkCorrectness(canvas):
    l = canvas.data["len"]
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    cnt = { }
    for row in range(rows):
        for col in range(cols):
            if(snakeBoard[col][row] > 0):
                cnt[snakeBoard[col][row]] = 1
    curlen = len(cnt)
    if(curlen == l):
        canvas.data["status"] = "on"
    else:
        canvas.data["status"] = "off"

def generateFood(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    x = canvas.data["food_posx"]
    y = canvas.data["food_posy"]
    if(x == - 1 and y == -1):
        while(1):
            x = random.randint(0, 9)
            y = random.randrange(0, 9)
            if(snakeBoard[x][y] == 0):
                break
    snakeBoard[x][y] = -1
    canvas.data["snakeBoard"] = snakeBoard
    canvas.data["food_posx"] = x
    canvas.data["food_posy"] = y
    redrawAll(canvas)

def timerFired(canvas):
    checkCorrectness(canvas)
    if(canvas.data["status"] == "off"):
        tkMessageBox.showinfo( "Snake", "Game Over your score " + str(canvas.data["len"]))
    else:
#        generateFood(canvas)
        redrawAll(canvas)
        delay = 250 # milliseconds
        moveSnake(canvas)
        canvas.after(delay, timerFired, canvas) # pause, then call timerFired again


def redrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)

def drawSnakeBoard(canvas):
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def drawSnakeCell(canvas, snakeBoard, row, col):
    margin = 5
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (snakeBoard[row][col] > 0):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    if(snakeBoard[row][col] < 0):
        canvas.create_oval(left, top, right, bottom, fill="black")

def loadSnakeBoard(canvas):
    snakeBoard = [ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0,-1, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                   [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                ]
    canvas.data["snakeBoard"] = snakeBoard

def printInstructions():
    print "Snake!"
    print "Use the arrow keys to move the snake."
    print "Eat food to grow."
    print "Stay on the board!"
    print "And don't crash into yourself!"

def init(canvas):
    canvas.data = { }
    canvas.data["status"] = "on"
    canvas.data["len"] = 1
    canvas.data["previous_posx"] = 0
    canvas.data["previous_posy"] = 1
    canvas.data["food_posx"] = 6
    canvas.data["food_posy"] = 6
    printInstructions()
    loadSnakeBoard(canvas)
    redrawAll(canvas)

def run():
    printInstructions
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=310, height=310)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    cnt = 0
    init(canvas)
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    cnt = cnt + 1
    timerFired(canvas)
    root.mainloop()
    # set up events
    root.mainloop()
    #print canvas.data["status"]
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
run()

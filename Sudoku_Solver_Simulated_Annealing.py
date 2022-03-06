import random
import time
import numpy as np
import math
from random import choice
import statistics

#checks the initial sudoku board for the original, fixed values
#and returns a board with those marked positions
def non_empty_boxes(sudokuClone):
    for i in range(9):
        for j in range(9):
            if sudokuClone[i, j] != 0:
                sudokuClone[i, j] = 1
    return sudokuClone

#returns a linear array indeces of each 3x3 block in the sudoku board
def sudoku_blocks():
    blockList = []

    for i in range(9):
        temp = []
        b1 = [k + 3 * ((i) % 3) for k in range(3)]
        b2 = [k + 3 * math.trunc((i) / 3) for k in range(3)]

        for n in b1:
            for m in b2:
                temp.append([n, m])
        blockList.append(temp)
    return blockList

#fill up all empty boxes with a random unique number from 1-10 within a 3x3 block
def randomly_fill_empty(sudoku, blockList):
    for block in blockList:
        for box in block:
            #if the current coord is empty
            if sudoku[box[0], box[1]] == 0:
                #grab the current block the current coord we're in
                current = sudoku[block[0][0]:(block[-1][0]+1), block[0][1]:(block[-1][1]+1)]

                #gives the empty box a random unique number within the current 3x3 block
                sudoku[box[0], box[1]] = choice([i for i in range(1, 10) if i not in current])
    return sudoku

#sums up total number of non-unique squares
def num_errors(sudoku):
    errors = 0
    for i in range(9):
        errors += row_column_errors(i, i, sudoku)
    return errors

#calculates the number of unique numbers in a row and column
#9 squares per row and column subtracted by # of unique numbers
def row_column_errors(row, column, sudoku):
    return (9 - len(np.unique(sudoku[:, column]))) + (9 - len(np.unique(sudoku[row, :])))

#simulated annealing temperature
def initial_temperature(sudoku, markedSudoku, blockList):
    list = []
    for i in range(9):
        sudoku = state(sudoku, markedSudoku, blockList)[0] #[board, coords]
        list.append(num_errors(sudoku))

    return statistics.pstdev(list)

#altered state of sudoku board
def state(sudoku, markedSudoku, blockList):
    randomBlock = random.choice(blockList) #chooses a random 3x3 block
    boxFlip = two_boxes(markedSudoku, randomBlock) #[[0, 1], [2, 1]]
    newSudoku = flip_boxes(sudoku, boxFlip) #returns the new, changed board
    return [newSudoku, boxFlip]

#chooses two random boxes on the sudoku board
def two_boxes(markedSudoku, randomBlock):
    while True:
        #choose random coord in the block
        box1 = random.choice(randomBlock)
        #choose another random coord in the block that isn't box1
        box2 = random.choice(randomBlock)
        while box2 == box1:
            box2 = random.choice(randomBlock)
      
        #choose boxes that are free to change (not the original fixed values)
        #otherwise, loop again and find different box values
        if markedSudoku[box1[0], box1[1]] != 1 and markedSudoku[box2[0], box2[1]] != 1:
            return [box1, box2]

#swaps the chosen boxes on the board and returns the new board
def flip_boxes(sudoku, boxFlip):
    newBoard = np.copy(sudoku)
    temp = newBoard[boxFlip[0][0], boxFlip[0][1]]
    newBoard[boxFlip[0][0], boxFlip[0][1]] = newBoard[boxFlip[1][0], boxFlip[1][1]]
    newBoard[boxFlip[1][0], boxFlip[1][1]] = temp
    return newBoard

def new_state(currentSudoku, markedSudoku, blockList, temperature):
    candidate = state(currentSudoku, markedSudoku, blockList) #gives a new board, and the coords of the flipped boxes
    newSudoku = candidate[0] #switches up the board = new sudoku board
    check = candidate[1] #the coords of the flipped spots. ex.) [[0, 1], [2, 0]]
    #cost of the current board
    currentFitness = row_column_errors(check[0][0], check[0][1], currentSudoku) + row_column_errors(check[1][0], check[1][1], currentSudoku)

    #cost of the new, swapped up board
    newFitness = row_column_errors(check[0][0], check[0][1], newSudoku) + row_column_errors(check[1][0], check[1][1], newSudoku)

    #Acceptance Probability Function P(e, e', T). If e' < e, and exp(-(e'-e)/T)
    p = math.exp(-(newFitness-currentFitness)/temperature) #e^(x)
    if(np.random.uniform(1, 0, 1) < p):
        return [newSudoku, (newFitness-currentFitness)]
    return [currentSudoku, 0]

def make_sudoku(sudoku, puzzle):
    for i in range(9):
        for j in range(9):
            sudoku[i][j] = puzzle[i][j]
    return sudoku

if __name__ == '__main__':
    #puzzle1 (Medium/Hard difficulty)
    puzzle1 = [[0,0,0,0,0,0,4,0,2],
               [6,0,0,7,0,0,0,1,0],
               [5,0,0,0,2,0,7,0,0],
               [0,3,0,0,1,0,0,4,8],
               [0,4,0,2,0,0,0,0,0],
               [0,8,0,9,0,0,0,5,0],
               [0,5,0,0,0,3,0,7,0],
               [0,0,0,0,0,0,0,0,0],
               [9,0,0,1,0,0,0,8,0]]

    #puzzle2 (Easy difficulty)
    puzzle = [[7,2,0,0,0,0,0,8,0],
              [0,0,0,4,8,0,0,2,6],
              [8,0,4,2,0,9,0,0,0],
              [0,8,2,0,1,5,0,3,0],
              [5,0,0,8,0,6,0,0,7],
              [0,0,0,9,0,0,0,5,0],
              [6,4,8,5,7,3,0,0,0],
              [0,0,5,0,0,0,0,0,0],
              [0,0,7,0,0,0,3,0,5]]

    #puzzle3 (Hard difficulty)
    puzzle3 = [[9,0,0,0,0,0,0,4,0],
              [0,0,6,3,0,0,9,0,0],
              [0,5,0,0,0,1,0,0,2],
              [8,0,0,0,7,0,0,0,4],
              [0,0,0,6,0,0,0,8,0],
              [0,0,0,0,0,0,7,9,0],
              [0,3,0,5,0,0,0,0,0],
              [0,0,1,0,0,6,0,0,0],
              [7,0,0,0,8,0,4,0,0]]

    tests = 10 #number of tests to run
    timeList = [] #list of time it takes to solve each run
    for i in range(tests):
        sudoku = np.zeros((9, 9)) #zero array of the board
        make_sudoku(sudoku, puzzle) #insert the values into the board
        print("\nInitial Puzzle")
        print(sudoku)

        coolingRate = 0.99
        struggle = 0
        markedSudoku = non_empty_boxes(np.copy(sudoku)) #board of fixed values
        blockList = sudoku_blocks() #2d linear array of 3x3 coords
        
        #empty slots are filled up with random values that are unique within a 3x3 block
        randomSudoku = randomly_fill_empty(sudoku, blockList)
        temperature = initial_temperature(sudoku, markedSudoku, blockList)
        fitness = num_errors(randomSudoku) #fitness/score of the board to determine if solved
      
        start = time.perf_counter()
        solved = False #while the sudoku board isn't solved
        print("\nSolving...")
        while not solved:
            lastFitness = fitness #holds the previous fitness value

            for i in range(20):
                #returns either a new changed board or the same board
                #also returns the difference of the newfitness and the originalfitness
                possibleState = new_state(randomSudoku, markedSudoku, blockList, temperature)

                randomSudoku = possibleState[0] #grabs the new (or same) board
                fitness += possibleState[1] #add the fitness difference
                #print(fitness)
                if fitness <= 0:
                    solved = True
                    break

            temperature *= coolingRate #cool the temperature down
            if fitness <= 0:
                solved = True
                break

            #if the fitness is worse than the last fitness, increment
            #the "struggle" factor
            if fitness >= lastFitness:
                struggle += 1
            else: #otherwise, we're not struggling so reset the struggle
                struggle = 0

            #if we're struggling a lot, then increase the temperature to
            #increase our "searching" range again
            if struggle > 75:
                temperature += 2

        end = time.perf_counter()
        print("\nSolved")
        print(randomSudoku)
        print("Time to Solve:", round(end-start, 2))
        timeList.append(round(end-start, 2))
    print("\nTimed Runs:", timeList)

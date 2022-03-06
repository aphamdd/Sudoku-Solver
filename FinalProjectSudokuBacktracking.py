import time
import copy

#we will need to find an empty pos to work on 
def find_empty_pos(board):
    #loop the 2d and find empty
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: #found empty
                #now will need to return the cords for the empty spot
                return (row, col) #will need to count for if no empty is found
    #outside of for loop no 0 was found
    return None #return no cords

#this function is the main solving function 
#this function will use backtracking
def solve_sudoku_backtrack(board):
    
    #first we will need to check for an empty space on the board
    if not find_empty_pos(board): #if there was no empty location found then return true the puzzle is solved
        return True
    else:#there is an empty location 
        #get the cords of the empty location
        row, col = find_empty_pos(board)
    #now once we have the empty location we need to test every possible number from 1 - 9
    for guess in range(1,10):
        #display_board(board)
        #print("****************************************")
        #now we will need to check if the number is possible to use
        if check_vaild(board, guess, row, col): #check if number in row and col valid 
            board[row][col] = guess  #vaild add
            #we will need to recurse to the next subproblem 
            if solve_sudoku_backtrack(board): #recursion 
                return True
            board[row][col] = 0 #resets back if guessus not correct 
    return False


def check_vaild(board, guess, new_row,new_col):
    #This function will check if the move is vaild 
    #we will need to follow basic rules of sudoku to check if move is valid
    # rule 1) we will need to check the 3x3 square if the guess is there and vaild (do this first this might take a bit)
    #rule 2) we need to check if vailid in row
    #rule 3) we need to check if vaild in col 
    #rule 1
    #need to check the inner box
    pos1 = new_row // 3 * 3 #this does int division which * 3 to find the cord
    pos2 = new_col // 3 * 3      
    #now we will need loop
    for i in range(pos1, pos1 + 3):
        for j in range(pos2, pos2+ 3):
            if board[i][j] == guess:
                return False
    #rule 2
    for row in range(9):
        if board[new_row][row] == guess:
            return False
    #rule 3
    for col in range(9):
        if board[col][new_col] == guess:
            return False
   
    return True


def display_board(board):
    for row in range(9):
        print(board[row])

if __name__:

    results = []
    
    sudoku_board_1=[[0,0,0,0,0,0,4,0,2],
                    [6,0,0,7,0,0,0,1,0],
                    [5,0,0,0,2,0,7,0,0],
                    [0,3,0,0,1,0,0,4,8],
                    [0,4,0,2,0,0,0,0,0],
                    [0,8,0,9,0,0,0,5,0],
                    [0,5,0,0,0,3,0,7,0],
                    [0,0,0,0,0,0,0,0,0],
                    [9,0,0,1,0,0,0,8,0]]

    sudoku_board_2=[[7,2,0,0,0,0,0,8,0],
                    [0,0,0,4,8,0,0,2,6],
                    [8,0,4,2,0,9,0,0,0],
                    [0,8,2,0,1,5,0,3,0],
                    [5,0,0,8,0,6,0,0,7],
                    [0,0,0,9,0,0,0,5,0],
                    [6,4,8,5,7,3,0,0,0],
                    [0,0,5,0,0,0,0,0,0],
                    [0,0,7,0,0,0,3,0,5]]

    sudoku_board_3=[[9,0,0,0,0,0,0,4,0],
                    [0,0,6,3,0,0,9,0,0],
                    [0,5,0,0,0,1,0,0,2],
                    [8,0,0,0,7,0,0,0,4],
                    [0,0,0,6,0,0,0,8,0],
                    [0,0,0,0,0,0,7,9,0],
                    [0,3,0,5,0,0,0,0,0],
                    [0,0,1,0,0,6,0,0,0],
                    [7,0,0,0,8,0,4,0,0]]

    print("This is board 1")
    display_board(sudoku_board_1)
    print("This is board 2")
    display_board(sudoku_board_2)
    print("This is board 3")
    display_board(sudoku_board_3)


    choice = input("enter the number sudoku puzzle you want ")
    num = int(choice)
    if(num == 1):
        print("solving in process")
        board_1 = []
        for i in range(10):
            #write about copying the master board to a diff board to make sure nothing happens to the master board
            board_1 = copy.deepcopy(sudoku_board_1)
            start = time.time()
            solve_sudoku_backtrack(board_1)
            end = time.time()
            dur = end - start
            results.append(dur)

        print(results)
        display_board(board_1)

    elif(num == 2):
        print("solving in process")
        board_2 = []
        for i in range(10):
            #write about copying the master board to a diff board to make sure nothing happens to the master board
            board_2 = copy.deepcopy(sudoku_board_2)
            start = time.time()
            solve_sudoku_backtrack(board_2)
            end = time.time()
            dur = end - start
            results.append(dur)
        print(results)
        display_board(board_2) 
        

    elif(num == 3):
        print("solving in process")
        board_3 = []
        for i in range(10):
            #write about copying the master board to a diff board to make sure nothing happens to the master board
            board_3 = copy.deepcopy(sudoku_board_3)
            start = time.time()
            solve_sudoku_backtrack(board_3)
            end = time.time()
            dur = end - start
            results.append(dur)

        print(results)
        display_board(board_3) 

time_avg = sum(results) /len(results)
print("avg time: ", time_avg)
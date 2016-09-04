import random
import copy
import sys

print('Welcome to Connect 4 game')
Width = 8
Height = 7
lookFurther=2

def main_game():

    while True:
        playerOption, computerOption = enterOption()
        initial_turn = turnDecider()
        print('The %s will make the first move.' % (initial_turn))
        mainBoard = createNewBoard()

        while True:
            if initial_turn == 'player':
                generateBoard(mainBoard)
                move = getPlayerMove(mainBoard)
                executeMove(mainBoard, playerOption, move)
                if isWinner(mainBoard, playerOption):
                    winner = 'player'
                    break
                initial_turn = 'computer'
            else:
                generateBoard(mainBoard)
                print('The computer is making its move...')
                move = getComputerMove(mainBoard, computerOption)
                executeMove(mainBoard, computerOption, move)
                if isWinner(mainBoard, computerOption):
                    winner = 'computer'
                    break
                initial_turn = 'player'

            if chkBoardFull(mainBoard):
                winner = 'tie'
                break

        generateBoard(mainBoard)
        print('The Winner of the game is: %s' % winner)
        if not playAgain():
            break

def enterOption():
    # Returns the list player's option as the first item, and the computer's option as the second.
    option = ''
    while not (option == 'X' or option == 'O'):
        print('Would you like to be X or O?')
        option = input().upper()
    if option == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def playAgain():
    # Return true if player wants to play again, False if not
    print('Press y to play again , n to quit')
    return input().lower().startswith('y')


def generateBoard(board):
    print()
    print(' ', end='')
    for x in range(1, Width + 1):
        print(' %s  ' % x, end='')
    print()

    print('#---#' + ('---#' * (Width - 1)))

    for y in range(Height):
        print('|   |' + ('   |' * (Width - 1)))

        print('|', end='')
        for x in range(Width):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (Width - 1)))

        print('#---#' + ('---#' * (Width - 1)))


def createNewBoard():
    board = []
    for x in range(Width):
        board.append([' '] * Height)
    return board


def getPlayerMove(Board):
    # run a loop till a valid option is entered by the user
    while True:
        print('Enter the column number in which you wish to place you option (1-%s) or press q to quit game)' % (Width))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(Board, move):
            return move

def getComputerMove(board, computerOption):
    # The static number 2 here means that the computer will look 2 moves further to chart the best course of action
    # Once a list of best possible moves is created , the computer randomly selects one for execution
    allPotentialMoves = getPotentialMoves(board, computerOption, lookFurther)
    highestMoveScore = max([allPotentialMoves[i] for i in range(Width) if isValidMove(board, i)])
    bestPossibleMoves = []
    for i in range(len(allPotentialMoves)):
        if allPotentialMoves[i] == highestMoveScore:
            bestPossibleMoves.append(i)
    return random.choice(bestPossibleMoves)


def getPotentialMoves(board, playerOption, lookBeyond):
    # Assigned Static values 1 for the best case ( potential win), 0 for tie, -1 for the worst case (potential loss)
    # looks further ahead by creating duplicate copies of boards at instances
    if lookBeyond == 0:
        return [0] * Width

    potentialMoves = []

    if playerOption == 'X':
        enemyOption = 'O'
    else:
        enemyOption = 'X'

    if chkBoardFull(board):
        return [0] * Width

    # Method to find the best move to take.
    # Initialize potential moves list with 0
    potentialMoves = [0] * Width
    for playerMove in range(Width):
        duplicateBoard = copy.deepcopy(board)
        if not isValidMove(duplicateBoard, playerMove):
            continue
        executeMove(duplicateBoard, playerOption, playerMove)
        if isWinner(duplicateBoard, playerOption):
            potentialMoves[playerMove] = 1
            break
        else:
            # do other player's moves and determine best one
            if chkBoardFull(duplicateBoard):
                potentialMoves[playerMove] = 0
            else:
                for enemyMove in range(Width):
                    duplicateBoard2 = copy.deepcopy(duplicateBoard)
                    if not isValidMove(duplicateBoard2, enemyMove):
                        continue
                    executeMove(duplicateBoard2, enemyOption, enemyMove)
                    if isWinner(duplicateBoard2, enemyOption):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(duplicateBoard2, playerOption, lookBeyond - 1)
                        potentialMoves[playerMove] += (sum(results) / Width) / Width
                       # print (potentialMoves[playerMove])
    return potentialMoves

def turnDecider():
    # Randomly chooses whether it will the computer who makes the first move or the player
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def executeMove(board, option, column):
    for y in range(Height-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = option
            return


def isValidMove(board, move):
    if move < 0 or move >= (Width):
        return False

    if board[move][0] != ' ':
        return False

    return True


def chkBoardFull(board):
    for x in range(Width):
        for y in range(Height):
            if board[x][y] == ' ':
                return False
    return True


def isWinner(board, option):
    # check for vertical case
    for x in range(Width):
        for y in range(Height - 3):
            if board[x][y] == option and board[x][y+1] == option and board[x][y+2] == option and board[x][y+3] == option:
                return True

    # check for horizontal case
    for y in range(Height):
        for x in range(Width - 3):
            if board[x][y] == option and board[x+1][y] == option and board[x+2][y] == option and board[x+3][y] == option:
                return True

    # check for diagonal ( left to right) case
    for x in range(Width - 3):
        for y in range(3, Height):
            if board[x][y] == option and board[x+1][y-1] == option and board[x+2][y-2] == option and board[x+3][y-3] == option:
                return True

    # check for diagonal ( right to left) case
    for x in range(Width - 3):
        for y in range(Height - 3):
            if board[x][y] == option and board[x+1][y+1] == option and board[x+2][y+2] == option and board[x+3][y+3] == option:
                return True

    return False

main_game()
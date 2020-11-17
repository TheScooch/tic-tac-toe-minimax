# Scott Gebert
# 1616526
# Assignment 6: OO Minimax


from math import inf as infinity
from random import choice
from random import seed as randomseed
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)

Scott Gebert
CCID: Sagebert

Credit to Paul Lu for base code
"""

class CurrState:
    """
    Creates an object to hold the state information as opposed to
    constantly passing it into functions
    :__init__ holds important varibles
    :retState returns the state
    """
    
    # Dictates the values for the human and comp
    HUMAN = -1
    COMP = +1

    # Initalizes the objects coords and state
    def __init__(self, x, y, state):  
        self.state = state
        self.coordinate = (x, y)
    
    def retState(self):
        """
        Not useful at the moment but can be used to return the 
        state of the board
        """
        return self.state 


class ticTacking:
    """
    Creates an object that takes care of all of the real processing, in this class
    numerous functions handle all nesseary tic-tak toe processes by manipulating a boarad 
    made up of a list of states with states being used to 
    """
    def __init__(self, choice_human, choice_ai):
        self.h_choice = choice_human
        self.c_choice = choice_ai
        self.boardMaker()

    def boardMaker(self):
        """
        This function creates the board by implmenting the CurrState class
        and creating one of these objects for each board position
        """
        self.board = []
        for ro in range(3):
            row = []
            for co in range(3):
                row.append(CurrState(ro , co, 0))
            self.board.append(row)


    def evaluate(self):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """

        # Changed params to use state class
        if self.wins(CurrState.COMP):
            score = +1
        elif self.wins(CurrState.HUMAN):
            score = -1
        else:
            score = 0

        return score


    def wins(self, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        
        # Added the self so it can call itself and the .state to be compatible with 
        # my new class
        win_state = [
            [self.board[0][0].state, self.board[0][1].state, self.board[0][2].state],
            [self.board[1][0].state, self.board[1][1].state, self.board[1][2].state],
            [self.board[2][0].state, self.board[2][1].state, self.board[2][2].state],
            [self.board[0][0].state, self.board[1][0].state, self.board[2][0].state],
            [self.board[0][1].state, self.board[1][1].state, self.board[2][1].state],
            [self.board[0][2].state, self.board[1][2].state, self.board[2][2].state],
            [self.board[0][0].state, self.board[1][1].state, self.board[2][2].state],
            [self.board[2][0].state, self.board[1][1].state, self.board[0][2].state],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False


    def game_over(self):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(CurrState.HUMAN) or self.wins(CurrState.COMP)


    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        # revamped how the cells list is created, it is now a list of 
        # objest as opposed to a list of locations, all of these objects
        # contain the location of an empty cell
        cells = []

        for lists in self.board:
            for ele in lists:
                if ele.state == 0:
                    cells.append(ele)
        return cells


    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        # Just added some selfs and changes some parms to make it work
        # within a class (removed most params and changed others to utlize the state 
        # object)
        if self.board[x][y] in self.empty_cells():
            return True
        else:
            return False


    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        # Just added some selfs and changes some parms to make it work
        # within a class (removed most params and changed others to utlize the state 
        # object)
        if self.valid_move(x, y):
            self.board[x][y].state = player
            return True
        else:
            return False


    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """

        # Just added some selfs and changes some parms to make it work
        # within a class (removed most params and changed others to utlize the state 
        # object)
        if player == CurrState.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell.coordinate
            self.board[x][y].state = player
            score = self.minimax( depth - 1, -player)
            self.board[x][y].state = 0
            score[0], score[1] = x, y

            if player == CurrState.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best


    def render(self):
        """
        Print the board on console
        :param state: current state of the board
        """

        chars = {
            -1: self.h_choice,
            +1: self.c_choice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in self.board:
            for cell in row:
                symbol = chars[cell.state]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)


    def ai_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        # Just added some selfs and changes some parms to make it work
        # within a class (removed most params and changed others to utlize the state 
        # object)
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        clean()
        print(f'Computer turn [{self.c_choice}]')
        self.render()

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, CurrState.COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, CurrState.COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)


    def human_turn(self):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        # Just added some selfs and changes some parms to make it work
        # within a class (removed most params and changed others to utlize the state 
        # object)
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        clean()
        print(f'Human turn [{self.h_choice}]')
        self.render()

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.set_move(coord[0], coord[1], CurrState.HUMAN)
                print(can_move)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')



# Not incluced in the other object as not realted to tic-tacking just clearing
def clean():
    """
    Clears the console
    """
    # Paul Lu.  Do not clear screen to keep output human readable.
    print()
    return

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def main():
    """
    Main function that calls all functions
    """
    # Paul Lu.  Set the seed to get deterministic behaviour for each run.
    #       Makes it easier for testing and tracing for understanding.
    randomseed(274 + 2020)

    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    # Creating the game object
    game = ticTacking(h_choice, c_choice)

    while len(game.empty_cells()) > 0 and not game.game_over():
        if first == 'N':
            game.ai_turn()
            first = ''

        game.human_turn()
        game.ai_turn()

    # Game over message
    if game.wins(CurrState.HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        game.render()
        print('YOU WIN!')
    elif game.wins(CurrState.COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        game.render()
        print('YOU LOSE!')
    else:
        clean()
        game.render()
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()

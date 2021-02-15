import numpy as np

from misc import legalMove
from misc import rowTest
from misc import diagTest
from misc import winningTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):

    def move(self, board):
        while True:
            # calculate best move location, if legal, return move location
            # call minimax root function to do this

            moveLoc = tuple()
            if legalMove(board, moveLoc):
                return moveLoc

    def minimaxroot(self, depth, game_position, is_max):
        best_move_location = (-100, -100)
        best_move_score = -9999
        # get a list of all possible moves from position

        # loop through all possible moves from game position
        # assume a possible move is made, this changes game_position

        # then we calculate the score returned from minimax function
        # passing depth-1, new game_position, !is_max as params

        # once score is calculated revert the game_position to what it was before

        # if greater than best_move_score, then update best_move_score and best_move_location

        # keep checking all possible moves from root until loop finished

        # finally return best_possible_move_location
        return best_move_location


    def minimax(self, depth, game_position, is_max):

        # check base case: is depth == to 0
        # if so, evaluate board, return (negative?)result of evaluation function taking in board info ()
        # in example its game.board() which is a 2d array of piece object,
        # we access the piece attributes to determine score
        # instead, we could simply take the current game_position (the board state)
        # check for evaluation features
        # the 2,3,4 uncovered, partial covered and sides (like in ipynb)

        if depth == 0:
            return eval(self.game_position)



        # get list of possible moves from game_position (board state)
        # a list of all positions (tuples) where value is 0, meaning unused

        if is_max:
            best_move_score = -9999
            # loop through all possible moves from game position
            # assume a move is made, this updates game_position (the board state)
            # best_move_score is:
            # the max between best_move_score and
            # the result of minimax call (depth-1, new game_position, !is_max)
            # revert the game_position/ board state
            # end loop

            return best_move_score

        else:
            best_move_score = 9999

            # loop through all possible moves from game position
            # assume a move is made, this updates game_position (the board state)
            # best_move_score is:
            # the max between best_move_score and
            # the result of minimax call (depth-1, new game_position, !is_max)
            # revert the game_position/ board state
            # end loop

            return best_move_score


    # eval is where the score is calculated
    # best to start small (count number of pieces placed in entire board, by player 1 and player 2)
    def eval(self, board):
        score = 0
        # loop through entire board, search for different features, add to score
        # this is where it we can use misc functions
        # e.g. finding 4 in a row:
        # rowtest(id, board, 4), diagtest(id, board, 4), then we rotate90 then call them again?

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                score += 0
                # could be score += getSides + get2U + get2P + get3U + get3P + get4U + get4P ...
        return score

    def getSides(self):
        return -1


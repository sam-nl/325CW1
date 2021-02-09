import numpy as np

from misc import legalMove
from misc import rowTest
from misc import diagTest
from misc import winningTest
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        win = self.getWinningMove(board)
        if(win):
            return win
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            print(moveLoc)
            if legalMove(board, moveLoc):
                return moveLoc
    
    #check if there is a move that will win the game and return it else return false
    def getWinningMove(self,board):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                check = (i,j)
                tempBoard = board
                if legalMove(tempBoard, check):
                    tempBoard[check] = self.ID
                    if(winningTest(self.ID, tempBoard, self.X_IN_A_LINE)):
                        return check
                    tempBoard[check] = 0
                
        return False
  
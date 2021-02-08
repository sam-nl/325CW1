import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        return board;
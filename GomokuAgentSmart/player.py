import numpy as np

from misc import legalMove
from misc import rowTest
from misc import diagTest
from misc import winningTest
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    p_2P = 1  # 2 in a row with one end covered
    p_2U = 5  # 2 in a row with neither end covered
    p_3P = 10  # 3 in a row
    p_3U = 50  # 3 in a row
    p_4P = 100  # 4 in a row
    p_4U = 1000  # 4 in a row
    p_5 = 5000

    def move(self, board):
        is_max = True
        while True:
            # calculate best move location, if legal, return move location
            # call minimax root function to do this
            moveLoc = self.minimaxroot(1, board, is_max)
            if legalMove(board, moveLoc):
                return moveLoc

    def addScore(self, arr):
        score = 0
        score += arr[0] * self.p_2P
        score += arr[1] * self.p_2U
        score += arr[2] * self.p_3P
        score += arr[3] * self.p_3U
        score += arr[4] * self.p_4P
        score += arr[5] * self.p_4U
        score += arr[6] * self.p_5
        return score

    def calculateScore(self, board):
        posLines = self.countLines(board, 1)
        negLines = self.countLines(board, -1)
        posScore = self.addScore(posLines)
        negScore = self.addScore(negLines)
        if self.ID == -1:
            posScore = posScore * 1.1
        else:
            negScore = negScore * 1.1
        score = posScore - negScore
        return score

    def countLines(self, board, ID1):
        count2P = 0
        count2U = 0
        count3P = 0
        count3U = 0
        count4P = 0
        count4U = 0
        count5 = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                pHoz = False
                uHoz = False
                pVer = False
                uVer = False
                pDia1 = False
                uDia1 = False
                pDia2 = False
                uDia2 = False
                lenCountHoz = 0
                lenCountVer = 0
                lenCountDia1 = 0
                lenCountDia2 = 0
                if board[i, j] == ID1:
                    # get hozlen
                    if j == 0 or board[i, j - 1] != ID1:
                        if j != 0 and board[i, j - 1] == 0:
                            pHoz = True
                        for k in range(5):
                            try:
                                if board[i, j + k] == ID1:
                                    lenCountHoz += 1
                                else:
                                    break
                            except IndexError:
                                pass
                            try:
                                if board[i, j + k + 1] == 0:
                                    if (pHoz):
                                        uHoz = True
                                        pHoz = False
                                    else:
                                        pHoz = True
                            except IndexError:
                                pass
                        if (lenCountHoz == 2):
                            if uHoz:
                                count2U += 1
                            if pHoz:
                                count2P += 1
                        elif (lenCountHoz == 3):
                            if uHoz:
                                count3U += 1
                            if pHoz:
                                count3P += 1
                        elif (lenCountHoz == 4):
                            if uHoz:
                                count4U += 1
                            if pHoz:
                                count4P += 1
                        elif (lenCountHoz == 5):
                            count5 += 1
                        # get verlen
                    if i == 0 or board[i - 1, j] != ID1:
                        if i != 0 and board[i - 1, j] == 0:
                            pVer = True
                        for k in range(5):
                            try:
                                if board[i + k, j] == ID1:
                                    lenCountVer += 1
                                else:
                                    break
                            except IndexError:
                                pass
                            try:
                                if board[i + k + 1, j] == 0:
                                    if (pVer):
                                        uVer = True
                                        pVer = False
                                    else:
                                        pVer = True
                            except IndexError:
                                pass
                        if (lenCountVer == 2):
                            if uVer:
                                count2U += 1
                            if pVer:
                                count2P += 1
                        elif (lenCountVer == 3):
                            if uVer:
                                count3U += 1
                            if pVer:
                                count3P += 1
                        elif (lenCountVer == 4):
                            if uVer:
                                count4U += 1
                            if pVer:
                                count4P += 1
                        elif (lenCountVer == 5):
                            count5 += 1
                    # get dia1 (down and right)
                    if i == 0 or board[i - 1, j - 1] != ID1:
                        if i != 0 and board[i - 1, j - 1] == 0:
                            pDia1 = True
                        for k in range(5):
                            try:
                                if board[i + k, j + k] == ID1:
                                    lenCountDia1 += 1
                                else:
                                    break
                            except IndexError:
                                pass
                            try:
                                if board[i + k + 1, j + k + 1] == 0:
                                    if (pDia1):
                                        uDia1 = True
                                        pDia1 = False
                                    else:
                                        pDia1 = True
                            except IndexError:
                                pass
                        if (lenCountDia1 == 2):
                            if uDia1:
                                count2U += 1
                            if pDia1:
                                count2P += 1
                        elif (lenCountDia1 == 3):
                            if uDia1:
                                count3U += 1
                            if pDia1:
                                count3P += 1
                        elif (lenCountDia1 == 4):
                            if uDia1:
                                count4U += 1
                            if pDia1:
                                count4P += 1
                        elif (lenCountDia1 == 5):
                            count5 += 1
                    # get dia2 (down and left)
                    if j + 1 == self.BOARD_SIZE or i == 0 or board[i - 1, j + 1] != ID1:
                        if j + 1 != self.BOARD_SIZE and i != 0 and board[i - 1, j + 1] == 0:
                            pDia2 = True
                        for k in range(5):
                            try:
                                if board[i + k, j - k] == ID1:
                                    lenCountDia2 += 1
                                else:
                                    break
                            except IndexError:
                                pass
                            try:
                                if board[i + k + 1, j - k - 1] == 0:
                                    if (pDia2):
                                        uDia2 = True
                                        pDia2 = False
                                    else:
                                        pDia2 = True
                            except IndexError:
                                pass
                        if (lenCountDia2 == 2):
                            if uDia2:
                                count2U += 1
                            if pDia2:
                                count2P += 1
                        elif (lenCountDia2 == 3):
                            if uDia2:
                                count3U += 1
                            if pDia2:
                                count3P += 1
                        elif (lenCountDia2 == 4):
                            if uDia2:
                                count4U += 1
                            if pDia2:
                                count4P += 1
                        elif (lenCountDia2 == 5):
                            count5 += 1
        return [count2P, count2U, count3P, count3U, count4P, count4U, count5]

    def minimaxroot(self, depth, game_position, is_max):
        best_move_location = (-100, -100)
        current_score = self.calculateScore(game_position)
        if is_max:
            best_move_score = -9999
        else:
            best_move_score = 9999
        temp_score = best_move_score
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                check = (i, j)
                new_game_position = game_position
                if legalMove(new_game_position, check):
                    new_game_position[check] = self.ID
                    if (is_max and self.calculateScore(new_game_position) > current_score):
                        temp_score = max(best_move_score,
                                         self.minimax(depth - 1, new_game_position, not is_max, -9999, 9999))
                        if (temp_score > best_move_score):
                            best_move_location = check;
                            best_move_score = temp_score

                    elif (self.calculateScore(new_game_position) < current_score):
                        temp_score = min(best_move_score,
                                         self.minimax(depth - 1, new_game_position, not is_max, -9999, 9999))
                        new_game_position[check] = 0
                        if (temp_score < best_move_score):
                            best_move_location = check;
                            best_move_score = temp_score

                    new_game_position[check] = 0
        return best_move_location

    def minimax(self, depth, game_position, is_max, alpha, beta):
        searching = True
        if depth == 0:
            return self.calculateScore(game_position)
        if is_max:
            best_move_score = -9999
            for i in range(self.BOARD_SIZE):
                if (searching == False):
                    break
                for j in range(self.BOARD_SIZE):
                    check = (i, j)
                    new_game_position = game_position
                    if legalMove(new_game_position, check):
                        new_game_position[check] = 1
                        best_move_score = max(best_move_score,
                                              self.minimax(depth - 1, new_game_position, not is_max, alpha, beta))
                        new_game_position[check] = 0
                        alpha = max(alpha, best_move_score)
                        if beta <= alpha:
                            searching = False
                            break
            return best_move_score

        else:
            best_move_score = 9999
            for i in range(self.BOARD_SIZE):
                if (searching == False):
                    break
                for j in range(self.BOARD_SIZE):
                    check = (i, j)
                    new_game_position = game_position
                    if legalMove(new_game_position, check):
                        new_game_position[check] = -1
                        best_move_score = min(best_move_score,
                                              self.minimax(depth - 1, new_game_position, not is_max, alpha, beta))
                        new_game_position[check] = 0
                        beta = min(beta, best_move_score)
                        if beta <= alpha:
                            searching = False
            return best_move_score

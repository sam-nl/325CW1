import numpy as np
from misc import legalMove
from misc import winningTest
from gomokuAgent import GomokuAgent
from queue import PriorityQueue
from time import time as time

class Player(GomokuAgent):
    def __init__(self, ID, BOARD_SIZE, X_IN_A_LINE):
        self.ID = ID
        self.BOARD_SIZE = BOARD_SIZE
        self.X_IN_A_LINE = X_IN_A_LINE
        self.board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), dtype=int)
        self.root = None
        self.current_node = None
        self.is_set = False
        self.centre = int(BOARD_SIZE/2)
        
    def move(self,board):
        move_loc = (0,0)
        if not self.is_set:                                         #if it is our first turn we must initialise
            first_move = self.first_move(board[:])                  #our first move can just be a precomputed central move
            self.current_node = self.root
        else:
            op_move = self.get_op_move(board[:])                          #else we should get the op's move and one move down the tree
            self.current_node = self.get_node(op_move)          
        self.board = board.copy()
        self.current_node.order_children()
        move_loc = (self.current_node.minimaxroot(4))               #grow the tree under the current board state
        #move_loc = (self.current_node.minimaxroot(5))
        if not self.is_set:
            self.is_set = True
            self.current_node = self.get_node(first_move)
            self.board[first_move] = self.ID
            return first_move
        else:
            self.current_node = self.get_node(move_loc)
            self.board[move_loc] = self.ID
            return move_loc
                        
    def get_op_move(self,board):
        diff = board-self.board
        diff_arr = np.stack(np.nonzero(diff),axis= -1)
        op_move = (diff_arr[0][0],diff_arr[0][1])
        return op_move
        
    def get_node(self, move_loc):                                   #check if the node is in the tree (it is one of our predicted moves)
        for child in self.current_node.children:
            if child.move_pos == move_loc:
                return child
        child = node(move_loc,self.current_node)                    #else make a new node under the last node
        self.current_node.children.append(child)
        return child
    
    def first_move(self,_board):                                    #initialises the root and makes the first move 
        my_first_move = (self.centre,self.centre)
        if not np.count_nonzero(_board):                            #the root is our move if the board is empty
            _board[my_first_move] = self.ID
            self.root = node(my_first_move, ID = self.ID,           
                             board = _board)
            return my_first_move                                    #we then return a central move as our first move
        else:                                                       #else the root is the opp's move
            op_first_move = self.get_op_move(_board)
            self.root = node(op_first_move, ID = -self.ID,
                             board = _board)
            if my_first_move != op_first_move:
                return my_first_move                                #return our first move, or next to it if that is taken
            else:
                return (self.centre-1,self.centre)

class node:      
    count = 0
    def __init__(self, move_pos, parent = None, ID = None, board = None, heur = False):
        self.minimax_score = None
        node.count += 1
        self.count = node.count - 0
        self.heu = heur
        self.move_pos = move_pos
        self.parent = parent
        self.children = []
        self.child_queue = PriorityQueue()
        self.board = []
        self.p_score = 0
        if parent == None:                                       #if no parent(root) initialise tree (run once per game)
            self.score = 0
            self.player_id = ID
            self.depth = 0
            self.empty_pieces = []
            for row in range(len(board)):
                for col in range(len(board)):
                    if board[row][col] == 0:
                        self.empty_pieces.append((row,col))
            self.board = board
            self.order_children()
                
        else:                                                     #we can gather info from our parent to save time re-computing it
            self.player_id = 0-self.parent.player_id
            self.depth = self.parent.depth+1
            self.empty_pieces = self.parent.empty_pieces.copy()
            self.board = self.parent.board.copy()
            try:
                self.empty_pieces.remove(self.move_pos)
            except: 
                pass
            self.board[self.move_pos] = self.player_id              #the nodes' board is one piece different to the parent'
            self.score_dif = self.get_score()
            self.score = self.parent.score + self.score_dif
        
    def order_children(self):
        self.child_queue = PriorityQueue()
        count = 0
        if self.children == []:
            for blank in self.empty_pieces:
                count -= 1
                heu = self.heuristic(blank)
                if heu > 0:
                    middle_pref = abs(blank[0]-5) + abs(blank[1]-5)
                    child = node(blank, self, heur = heu)  
                    self.children.append(child)
                    self.child_queue.put((child.player_id*(heu+abs(child.score)+abs(child.p_score)),middle_pref,count,child))
        else:
            for child in self.children:
                count -= 1
                middle_pref = abs(child.move_pos[0]-5) + abs(child.move_pos[1]-5)
                self.child_queue.put((child.player_id*(child.heu+abs(child.score)+abs(child.p_score)),middle_pref,count,child))
        
    def heuristic(self, coords):
        score = 0
        for x in range(-1,2):
            for y in range(-1,2):
                try:
                    if self.board[coords[0]+x][coords[1]+y]!=0:
                        score+=1
                except:
                    pass
        return score
    
    def get_score(self):
        p_3 = 10
        u_3 = 50
        p_4 = 100
        u_4 = 20000
        score_5 = 50000
        score = 0
        added, removed, prevented = self.evaluate()
        for i in added:
            if i[0] == 3:
                if i[1] == 1:
                    score += p_3*i[2]
                else:
                    score += u_3*i[2]
            elif i[0] == 4:
                if i[1] == 1:
                    score += p_4*i[2]
                else:
                    score += u_4*i[2]
            elif i[0] == 5:
                score += score_5*i[2]
        for i in removed:
            if i[0] == 3:
                if i[1] == 1:
                    score -= p_3*i[2]
                else:
                    score -= u_3*i[2]
            elif i[0] == 4:
                if i[1] == 1:
                    score -= p_4*i[2]
                else:
                    score -= u_4*i[2]
            elif i[0] == 5:
                score -= score_5*i[2]
        for i in prevented:
            if i[0] == 3:
                self.p_score -= u_3*i[2]
            elif i[0] == 4:
                self.p_score -= u_4*i[2]
            elif i[0] == 5:
                self.p_score -= score_5*i[2]
        return score
        
    def get_next(self,pos,direction):                       #returns the id and position of the next cell in the line in tuple
            try:
                next_place = (pos[0]+direction[0],pos[1]+direction[1])
                return (self.board[next_place],next_place)
            except:
                return (2,next_place)
    
    def evaluate(self):
        lines_made = []
        lines_removed = []
        lines_prevented = []
        end_list = []
        for x in range(-1,2):                                  
            for y in range(-1,2):
                if x != 0 or y != 0:                                     #for each location next to our move (not on it)
                    length = 0
                    open_ends = 0
                    centre = (self.board[self.move_pos[0]][self.move_pos[1]],self.move_pos) 
                    end1 = self.get_next(centre[1],(x,y))
                    end2 = centre
                    cur_id = end1[0]
                    middle = False
                    if end1[0] != 0 and end1[0] != 2:                          #if the location isnt empty or a side

                        while end1[0] == cur_id:                               #go along and get the length in the + direction
                            end1 = self.get_next(end1[1],(x,y))
                            length+=1
                        if cur_id == self.player_id:                                
                            if self.get_next(end2[1],(-x,-y))[0] == self.player_id:       #if the piece on the other side of the centre piece is our piece
                                middle = True                                   #we have put a piece in the middle of the created line
                            while end2[0] == cur_id:                            #we then have to go back the other way and find that length
                                end2 = self.get_next(end2[1],(-x,-y))                
                                length+=1
                        else:                                                  #else we are blocking an opponent's line
                            if self.get_next(end2[1],(-x,-y))[0] == self.player_id:     #we block the whole line and not 2 short lines e.g 11-111 blocks a 5
                                middle = True                                  #not 2 length 2s
                                end2 = self.get_next(end2[1],(-x,-y))
                                length+=1
                                while end2[0] == cur_id:
                                    end2 = self.get_next(end2[1],(-x,-y))
                                    length += 1
                            else:
                                b_len = length
                                middle = True                                  
                                b_end2 = self.get_next(end2[1],(-x,-y))
                                b_len+=1
                                while end2[0] == cur_id:
                                    b_end2 = self.get_next(end2[1],(-x,-y))
                                    b_len += 1
                                b_end2 = self.get_next(end2[1],(-x,-y))
                                if end1[0] == 0:
                                    open_ends+=1
                                if end2[0] == 0:
                                    open_ends+=1
                                lines_prevented.append((b_len,open_ends,cur_id))
                                open_ends = 0  

                        if end1[0] == 0:
                            open_ends+=1
                        if end2[0] == 0:
                            open_ends+=1
                        if length>2 and ((end1 not in end_list and end2 not in end_list) or end2 == centre):
                            if length == 3 and open_ends >1:
                                lines_made.append((length,open_ends,cur_id))
                            elif open_ends > 0:
                                lines_made.append((length,open_ends,cur_id))
                            elif length == 5:
                                lines_made.append((length,open_ends,cur_id))
                            if length<5:
                                if cur_id != self.player_id and open_ends<2:
                                    lines_removed.append((length,open_ends+1,cur_id))
                                elif not middle and length > 3:
                                    lines_removed.append((length-1,open_ends,cur_id))
                            end_list.append(end1)
                            end_list.append(end2)
        return (lines_made,lines_removed,lines_prevented)
    
    def minimaxroot(self, depth):
        best_move_location = (0, 0)
        current_score = self.score
        if self.player_id == -1:
            best_move_score = -99999
        else:
            best_move_score = 99999
        self.order_children()
        time_out = time()
        while not self.child_queue.empty() and time()-time_out< 4:
            child = self.child_queue.get()
            #print(child)
            #child = child[3]
            #print(child.move_pos)
            if (child.player_id == 1):
                temp_score = max(best_move_score,child.minimax(depth-1,-99999,99999))
                if (temp_score > best_move_score): 
                    best_move_location = child.move_pos;
                    best_move_score = temp_score
                    print(child.p_score)
                    if child.p_score >= 10000:
                        return best_move_location
                    
            else:
                temp_score = min(best_move_score,child.minimax(depth-1,-99999,99999))
                if (temp_score < best_move_score):
                    best_move_location = child.move_pos;
                    best_move_score = temp_score
                    print(child.p_score)
                    if child.p_score <= -10000:
                        return best_move_location
        return best_move_location
    
    def minimax(self,depth, alpha, beta):
        if depth <= 0:
            return self.score + self.p_score
        self.order_children()
        best_move_score = 99999*self.player_id
        count = 6
        while not self.child_queue.empty() and count>0:
            count -= 1
            child = self.child_queue.get()
            child = child[3]
            if child.player_id == 1:
                self.minimax_score = child.minimax(depth-1, alpha,beta)
                best_move_score = max(best_move_score,self.minimax_score)
                alpha = max(alpha, best_move_score)
                if beta <= alpha:
                    break
            else:
                self.minimax_score = child.minimax(depth-1, alpha,beta)
                best_move_score = min(best_move_score,self.minimax_score)
                beta = min(beta, best_move_score)
                if beta <= alpha:
                    break
        return best_move_score
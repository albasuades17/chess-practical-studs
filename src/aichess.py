#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""

import chess
import numpy as np
import sys

from itertools import permutations


class Aichess():

    """
    A class to represent the game of chess.

    ...

    Attributes:
    -----------
    chess : Chess
        represents the chess game

    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece



    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 7;


    def getCurrentState(self):
    
        return self.myCurrentStateW
    
    
    def getListNextStatesW(self, myState):
    
        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()

        return self.listNextStates


    def isSameState(self, a, b):
        
        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):
            
            if a[k] not in b:
                isSameState1 = False
                
        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):
            
            if b[k] not in a:
                isSameState2 = False
        
        isSameState = isSameState1 and isSameState2
        return isSameState
    
    
    def isVisited(self, mystate):
    
        if (len(self.listVisitedStates)>0):
            perm_state = list(permutations(mystate))
            
            isVisited = False
            for j in range(len(perm_state)):
    
                for k in range(len(self.listVisitedStates)):
                    
                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        
                        isVisited = True
            
            return isVisited
        else:
            return False


    def isCheckMate(self, mystate):
        
        #listCheckMateStates = [[[4,5,2],[0,7,2]],[[4,5,2],[1,7,2]],[[4,5,2],[2,7,2]],[[4,5,2],[6,7,2]],[[4,5,2],[7,7,2]]]

        #posem els possibles estats on es produeixi check mate
        listCheckMateStates = [[[0,0,2],[2,4,6]],[[0,1,2],[2,4,6]],[[0,2,2],[2,4,6]],[[0,6,2],[2,4,6]],[[0,7,2],[2,4,6]]]

        if mystate in listCheckMateStates or mystate.reverse() in listCheckMateStates:
            print("Check mate --- ",mystate)
            return True
        else:
            return False


    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """

        #Si no hem arribat a la profunditat màxima
        if depth < self.depthMax:
            #si no hem visitat aquest estat
            if not currentState in self.listVisitedStates:
                self.listVisitedStates.append(currentState)
                #mirem si és checkmate
                if self.isCheckMate(currentState):
                    self.pathToTarget.append(currentState)
                    print("found")
                    print(currentState)

                else:
                    #print(currentState, depth)
                    #print(self.getListNextStatesW(currentState))
                    for son in self.getListNextStatesW(currentState):
                        #si ens posen primer la posició del rei, la invertim
                        if son[0][2] == 6:
                            fitxaMoguda = 1
                            son.reverse()
                        else:
                            fitxaMoguda = 0

                        #comprovem que l'estat no l'haguem visitat
                        if not son in self.listVisitedStates:

                            self.chess.moveSim(currentState[fitxaMoguda], son[fitxaMoguda])
                            self.chess.boardSim.print_board()
                            self.DepthFirstSearch(son, depth + 1)
                            self.chess.moveSim(son[fitxaMoguda], currentState[fitxaMoguda])



                            if len(self.pathToTarget) > 0:
                                self.pathToTarget.insert(0, currentState)
                                break





                    """
                
                        if not son in self.listVisitedStates and not son.reverse() in self.listVisitedStates:
                            son.reverse()
                            if son[0][2] == currentState[0][2]:
                                fitxaMoguda = currentState[0]
                            else:
                                fitxaMoguda = currentState[1]

                            print(fitxaMoguda, son[0], depth)
                            self.chess.moveSim(fitxaMoguda,son[0])
                            print("ja s'ha mogut")
                            self.chess.boardSim.print_board()
                            self.DepthFirstSearch(son, depth + 1)
                            print("soc el pare")
                            print(fitxaMoguda, son[0], depth)
                            self.chess.moveSim(son[0], fitxaMoguda)

                        if len(self.pathToTarget) > 0:
                            self.pathToTarget.insert(0, currentState)
                            break
                            
                                        """














    
        # for you to fill in

        # all tree explored, no check mate found
        #else:
    
            #return False
        
        

    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        
        # your code
        return
            
        
        
        
        

def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """

    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            print(s[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(s[1] + "is not in the range from a - h")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None







if __name__ == "__main__":

 #   if len(sys.argv) < 2:
 #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    # white pieces
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12
    

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()

    print("printing board")
    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State",currentState)
    
    # it uses board to get them... careful 
    aichess.getListNextStatesW(currentState)
    print("list next states ",aichess.listNextStates)

 #
    curr = aichess.getListNextStatesW(currentState)[0]
    #aichess.chess.moveSim(currentState[0],curr[0])
    #list = aichess.getListNextStatesW(curr)
    #print(list)
 #

    
    # starting from current state find the end state (check mate) - recursive function
    aichess.chess.boardSim.listVisitedStates = []
    # find the shortest path, initial depth 0
    depth = 0
    aichess.DepthFirstSearch(currentState, depth)
    print(aichess.pathToTarget)

    print("DFS End")

    MovesToMake = ['1e','2e','2e','3e','3e','4d','4d','3c']

    for k in range(int(len(MovesToMake)/2)):

        print("k: ",k)

        print("start: ",MovesToMake[2*k])
        print("to: ",MovesToMake[2*k+1])

        start = translate(MovesToMake[2*k])
        to = translate(MovesToMake[2*k+1])

        print("start: ",start)
        print("to: ",to)

        aichess.chess.moveSim(start, to)


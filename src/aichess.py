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
        self.depthMax = 3;#8
        self.checkMate = False
        self.BFSQueue = []

        #Farem un diccionari per controlar els estats visitats i en quina profunditat s'han trobat
        #self.dictVisitedStates = {}
        #Diccionari per reconstruir el camí BFS
        self.dictPath = {}


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

        if (len(self.listVisitedStates) > 0):
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
        #posem els possibles estats on es produeixi check mate
        listCheckMateStates = [[[0,0,2],[2,4,6]],[[0,1,2],[2,4,6]],[[0,2,2],[2,4,6]],[[0,6,2],[2,4,6]],[[0,7,2],[2,4,6]]]

        #Mirem totes les permutacions de l'estat i si coincideixen amb la llista de CheckMates
        for permState in list(permutations(mystate)):
            if list(permState) in listCheckMateStates:
                return True

        return False

    """
    def worthExploring(self, state, depth):
        #Primer de tot comprovem que la profunditat superi depthMax
        if depth > self.depthMax: return False
        visited = False
        #Comprovem si l'estat ha estat visitat
        for perm in list(permutations(state)):
            permStr = str(perm)
            if permStr in list(self.dictVisitedStates.keys()):
                visited = True
                #Si ha estat visitat amb una profunditat major a l'actual, ens interessa tornar a visitar-lo
                if depth < self.dictVisitedStates[perm]:
                    #Actualitzem la profunditat de l'estat
                    self.dictVisitedStates[permStr] = depth
                    return True
        #Si no l'hem visitat l'afegim al diccionari amb la profunditat actual
        if not visited:
            permStr = str(state)
            self.dictVisitedStates[permStr] = depth
            return True
    """

    def DFS(self, currentState, depth):
        self.listVisitedStates.append(currentState)

        if self.isCheckMate(currentState):
            self.pathToTarget.append(currentState)
            return True

        if depth < self.depthMax:
            for son in self.getListNextStatesW(currentState):
                if not self.isVisited(son):
                    if son[0][2] == currentState[0][2]:
                        fitxaMoguda = 0
                    else:
                        fitxaMoguda = 1

                    self.chess.moveSim(currentState[fitxaMoguda],son[0])
                    if self.DFS(son,depth+1):
                        self.pathToTarget.insert(0,currentState)
                        return True
                    self.chess.moveSim(son[0],currentState[fitxaMoguda])

        self.listVisitedStates.remove(currentState)


    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        #hem visitat el node, per tant l'afegim a la llista
        self.listVisitedStates.append(currentState)

        if depth >= self.depthMax:
            return 0

        #mirem si és checkmate
        if self.isCheckMate(currentState):
            self.pathToTarget.append(currentState)
            return 1

        else:
            for son in self.getListNextStatesW(currentState):
                if not self.isVisited(son):
                    #en l'estat son, la primera peça és la que s'ha mogut
                    #Mirem a quina posició de currentState correspon la fitxa moguda
                    if son[0][2] == currentState[0][2]:
                        fitxaMoguda = 0
                    else:
                        fitxaMoguda = 1


                    #movem la fitxa a la nova posició
                    self.chess.moveSim(currentState[fitxaMoguda], son[0])

                    #Cridem un altre cop el mètode amb el fill i augmentant la profunditat
                    if self.DepthFirstSearch(son, depth + 1):
                        self.pathToTarget.insert(0,currentState)
                    #tornem a posar el taulell en la seva posició anterior
                    self.chess.moveSim(son[0], currentState[fitxaMoguda])

                    #si ja hem trobat l'estat per fer checkMate, afegim a la llista els anteriors estats
                    if len(self.pathToTarget) > 0:
                        self.pathToTarget.insert(0, currentState)
                        break


    def reconstructPath(self, state, depth):
        #Quan ja hem trobat la solució, obtenim el camí seguit per arribar a aquesta
        for i in range(depth):
            self.pathToTarget.insert(0,state)
            #Per cada node, mirem quin és el seu pare
            state = self.dictPath[str(state)][0]

        self.pathToTarget.insert(0,state)

    def canviarEstat(self, start, to):
        #Veiem quina fitxa s'ha mogut d'un estat a un altre
        if start[0] == to[0]:
            fitxaMogudaStart=1
            fitxaMogudaTo = 1
        elif start[0] == to[1]:
            fitxaMogudaStart = 1
            fitxaMogudaTo = 0
        elif start[1] == to[0]:
            fitxaMogudaStart = 0
            fitxaMogudaTo = 1
        else:
            fitxaMogudaStart = 0
            fitxaMogudaTo = 0
        # movem la fitxa canviada
        self.chess.moveSim(start[fitxaMogudaStart], to[fitxaMogudaTo])

    def movePiecesBFS(self, start, depthStart, to, depthTo):
        #Per moure d'un estat a un altre al BFS necessitem trobar l'estat en comú, i llavors moure'ns fins al node to
        moveList = []
        #Si les depth's no són igual, retrocedim al node pare del nodeTo, per estar al mateix nivell
        nodeTo = to
        nodeStart = start
        while(depthTo > depthStart):
            moveList.insert(0,to)
            nodeTo = self.dictPath[str(nodeTo)][0]
            depthTo-=1
        while(depthStart > depthTo):
            ancestreStart = self.dictPath[str(nodeStart)][0]
            # Movem la fitxa del taulell a l'estat pare del nodeStart
            self.canviarEstat(nodeStart, ancestreStart)
            nodeStart = ancestreStart
            depthStart -= 1

        moveList.insert(0,nodeTo)
        #Busquem node en comú
        while nodeStart != nodeTo:
            ancestreStart = self.dictPath[str(nodeStart)][0]
            #Movem la fitxa del taulell a l'estat pare del nodeStart
            self.canviarEstat(nodeStart,ancestreStart)
            #Agafem el pare de nodeTo
            nodeTo = self.dictPath[str(nodeTo)][0]
            #El guardem a la llista
            moveList.insert(0,nodeTo)
            nodeStart = ancestreStart
        #Movem les fitxes des del node en comú fins el node to
        for i in range(len(moveList)):
            if i < len(moveList) - 1:
                self.canviarEstat(moveList[i],moveList[i+1])



    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW
        """
        #Si és el node arrel, l'afegim a visitats
        if depth == 0:
           self.listVisitedStates.append(currentState)
        #Comprovem que la profunditat no superi depthMax per si de cas
        if depth <= self.depthMax:
            # mirem si és checkmate
            if self.isCheckMate(currentState):
                self.reconstructPath(currentState,depth)
                return True

            else:
                for son in self.getListNextStatesW(currentState):
                    if not self.isVisited(son):
                        self.listVisitedStates.append(son)
                        #Afegim el fill no visitat a la cua
                        self.BFSQueue.append(son)
                        #guardem al diccionari el pare de cada node fill
                        self.dictPath[str(son)] = (currentState,depth)

                #agafem el primer node que hem afegit de la llista
                node = self.BFSQueue.pop(0)

                if node != None:
                    depthNextNode = self.dictPath[str(node)][1]+1
                    self.movePiecesBFS(currentState,depth,node,depthNextNode)
                    self.BreadthFirstSearch(node, depthNextNode)

        return False
        # your code

    def h(self,state):
        if state[0][2] == 2:
            posicioRei = state[1]
            posicioTorre = state[0]
        else:
            posicioRei = state[0]
            posicioTorre = state[1]
        #Amb el rei volem arribar a la configuració (2,4). Calculem la distància Manhattan
        fila = abs(posicioRei[0] - 2)
        columna = abs(posicioRei[1]-4)
        #Agafem el mínim de la fila i la columna, això és per quan el rei s'ha de moure en diagonal
        #Fem la diferència entre fila i columna, amb això calcularem els moviments restants que ha de fer anant recte
        hRei = min(fila, columna) + abs(fila-columna)
        #Amb la torre tenim 3 casos diferents
        if posicioTorre[0] == 0 and (posicioTorre[1] < 3 or posicioTorre[1] > 5):
            hTorre = 0
        elif posicioTorre[0] != 0 and posicioTorre[1] >= 3 and posicioTorre[1] <= 5:
            hTorre = 2
        else:
            hTorre = 1
        #En el nostre cas, l'heurística és el càlcul real del cost dels moviments.
        #Ho hem pogut fer perquè era fàcil de calcular.
        return hRei + hTorre

    def AStarSearch(self, currentState):
        frontera = []
        frontera.append((self.h(currentState),currentState))
        #El node arrel no té pare, per tant afegim None, i -1, que seria la depth del "node pare"
        self.dictPath[str(currentState)] = (None, -1)
        depthCurrentState = 0
        #anem iterant fins que ja no tinguem nodes candidats
        while len(frontera) > 0:
            #Ordenem segons la funció que suma el cost fins el node actual, i l'heurística
            frontera.sort()
            #Treiem la configuració més òptima
            nodeState = frontera.pop(0)
            node = nodeState[1]
            depthNode = self.dictPath[str(node)][1] + 1
            #Si no és el node arrel, movem les peces de l'estat anterior a l'actual
            if depthNode > 0:
                self.movePiecesBFS(currentState,depthCurrentState,node, depthNode)

            if self.isCheckMate(node):
                #Si és checkmate, construïm el camí que hem trobat més òptim
                self.reconstructPath(node,depthNode)
                break

            self.listVisitedStates.append(node)
            for son in self.getListNextStatesW(node):
                if not self.isVisited(son):
                    #Calculem el cost per arribar a la solució
                    costTotal = depthNode + 1 + self.h(son)
                    frontera.append((costTotal,son))
                    self.dictPath[str(son)] = (node,depthNode)
            currentState = node
            depthCurrentState = depthNode



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
    TA[4][4] = 6
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
    print("list next states ", aichess.listNextStates)

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    #aichess.DepthFirstSearch(currentState, depth)
    #aichess.DFS(currentState, depth)

    print(aichess.pathToTarget)
    print("DFS End")

    depth = 0
    aichess.BreadthFirstSearch(currentState, depth)
    print(aichess.pathToTarget)
    print("BFS End")

    #aichess.AStarSearch(currentState)
    print("A* End")

    # example move piece from start to end state
    MovesToMake = ['1e', '2e']
    print("start: ", MovesToMake[0])
    print("to: ", MovesToMake[1])

    start = translate(MovesToMake[0])
    to = translate(MovesToMake[1])

    print("start: ", start)
    print("to: ", to)

    aichess.chess.moveSim(start, to)

    # aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    #print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.board.currentStateW)

    """
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
    """


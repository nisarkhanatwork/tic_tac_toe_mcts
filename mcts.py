import random as random
from datetime import datetime
import math
import sys

INTEGER_MIN_VALUE = -2147483648
INTEGER_MAX_VALUE = sys.maxsize

def show_call_and_return_details(f):
    """
    for debugging
    """
    func_name = f.__name__
    def execute_extra(*x, **kw):
        call_string = "{}".format(func_name)
        #print(">>> Calling " + call_string)
        result = f(*x, **kw)
        #print("<<< Returning {} from ".format(result) + call_string)
        return result
    return execute_extra

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
        
    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y

class Board:
    DEFAULT_BOARD_SIZE = 3
    P1 = 1
    P2 = 2
    DRAW = 0
    IN_PROGRESS = -1 
    
    def __init__(self):
        self.boardValues = [[0 for _ in range( self.DEFAULT_BOARD_SIZE)] for _ in range( self.DEFAULT_BOARD_SIZE)]
        self.totalMoves = 0

    @show_call_and_return_details
    def performMove(self, player, p):
        self.totalMoves += 1
        self.boardValues[p.getX()][p.getY()] = player

    @show_call_and_return_details
    def getBoardValues(self):
        return self.boardValues

    def setBoardValues(self, boardValues):
        self.boardValues = boardValues    

    def printArr(self, arr):
        print(arr)

    @show_call_and_return_details
    def checkStatus(self):
        boardSize = len(self.boardValues)
        maxIndex = boardSize - 1 

        diag1 = [0] * boardSize   
        diag2 = [0] * boardSize   

        for i in range(boardSize):
            row = self.boardValues[i]
            col = [0] * boardSize
            for j in range(boardSize):
                col[j] = self.boardValues[j][i]

            checkRowForWin = self.checkForWin(row)
            if(checkRowForWin != 0):
                return checkRowForWin
            
            checkColForWin = self.checkForWin(col)
            if(checkColForWin != 0):
                return checkColForWin

            diag1[i] = self.boardValues[i][i]
            diag2[i] = self.boardValues[maxIndex - i][i]

        checkDiag1ForWin = self.checkForWin(diag1)
        if(checkDiag1ForWin != 0):
            return checkDiag1ForWin
        
        checkDiag2ForWin = self.checkForWin(diag2)
        if(checkDiag2ForWin != 0):
            return checkDiag2ForWin

        if(len(self.getEmptyPositions()) > 0):
            return self.IN_PROGRESS
        else:
            return self.DRAW


    def checkForWin(self, row):
        isEqual = True
        size = len(row)
        previous = row[0]
        
        for i in range(size):
            if(previous !=  row[i]):
                isEqual = False
                break
            previous = row[i]

        if(isEqual == True):
            return previous
        else:
            return 0


    def printBoard(self):
        size = len(self.boardValues)
        for i in range(size):
            for j in range(size):
                print(self.boardValues[i][j] + " ", end='')
            print("")

    @show_call_and_return_details
    def getEmptyPositions(self):
        size = len(self.boardValues)
        emptyPositions = []
        for i in range(size):
            for j in range(size):
                if(self.boardValues[i][j] == 0):
                    emptyPositions.append(Position(i, j))
        return emptyPositions

    def printStatus(self):
        status = self.checkStatus()
        if(status == P1):
            print("Player 1 wins")
        elif(status == P2):
            print("Player 2 wins")
        elif(status == DRAW):
            print("Game Draw")
        elif(status == IN_PROGRESS):
            print("Game in Progress")
        else: 
            print("Wrong Game State:Error")

    def printBoard(self):
        print("=========")
        for i in range(len(self.boardValues)):
            for j in range(len(self.boardValues)):
                print(self.boardValues[i][j], end = "")
                if(j < len(self.boardValues) - 1):
                    print("---", end = "")
            print("")
        print("=========")

    def setMembersBoardSize(self, boardSize):
        self.boardValues = [[0 for _ in range(boardSize)] for _ in range(boardSize)]

    def setMembersBoardValues(self, boardValues):
        self.boardValues = boardValues

    def setMembersTotalMoves(self, boardValues, totalMoves):
        self.boardValues = boardValues
        self.totalMoves = totalMoves

    @show_call_and_return_details
    def setMembersBoard(self, board):
        boardLength = len(board.getBoardValues())
        self.boardValues = [[0 for _ in range(boardLength)] for _ in range(boardLength)]
        boardValues = board.getBoardValues()
        n = len(boardValues)
        for i in range(n):
            m = len(boardValues[i])    
            for j in range(m):
                self.boardValues[i][j] = boardValues[i][j]

    

class State:
    def __init__(self):
        self.board = Board()
        self.visitCount = 0
        self.winScore = 0
        self.playerNo = Board.P1 # have to see how this works

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getPlayerNo(self):
        return self.playerNo

    def setPlayerNo(self, playerNo):
        self.playerNo = playerNo

    def getOpponent(self):
        return 3 - self.playerNo

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self, visitCount):
        self.visitCount = visitCount

    def getWinScore(self):
        return self.winScore

    def setWinScore(self, winScore):
        self.winScore = winScore

    @show_call_and_return_details
    def getAllPossibleStates(self):
        possibleStates = []
        availablePositions = self.board.getEmptyPositions()
        for i in range(len(availablePositions)):
            newState = State()
            newState.setMembersBoard(self.board)
            newState.setPlayerNo(3 - self.playerNo)
            newState.getBoard().performMove(newState.getPlayerNo(), availablePositions[i])
            possibleStates.append(newState)
        return possibleStates

    def incrementVisit(self):
        self.visitCount += 1

    def addScore(self, score):
        if(self.winScore != INTEGER_MIN_VALUE):
            self.winScore += score

    @show_call_and_return_details
    def randomPlay(self):
        availablePositions = self.board.getEmptyPositions()
        totalPosibilities = len(availablePositions)
        selectRandom = random.randrange(totalPosibilities)
        self.board.performMove(self.playerNo, availablePositions[selectRandom])

    def togglePlayer(self):
        self.playerNo = 3 - self.playerNo
       
    @show_call_and_return_details
    def setMembersState(self, state):
        self.board = Board()
        self.board.setMembersBoard(state.getBoard())
        self.playerNo = state.getPlayerNo()
        self.visitCount = state.getVisitCount()
        self.winScore = state.getWinScore()
    
    def setMembersBoard(self, board):
        self.board = Board()
        self.board.setMembersBoard(board)
        
class Node:
    
    def __init__(self):
        self.state = State()
        self.childArray = []
        self.parent = None
    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state

    def getParent(self):
        return self.parent
    
    def setParent(self, parent):
        self.parent = parent

    def getChildArray(self):
        return self.childArray

    def setChildArray(self, childArray):
        self.childArray = childArray

    @show_call_and_return_details
    def getRandomChildNode(self):
        noOfPossibleMoves = len(self.childArray)
        selectRandom = random.randrange(noOfPossibleMoves)
        return self.childArray[selectRandom]

    @show_call_and_return_details
    def getChildWithMaxScore(self):
        arr = [ x.getState().getVisitCount() for x in self.childArray]
        if(len(arr) == 0):
            return self 
        else:
            return self.childArray[arr.index(max(arr))]
    
    @show_call_and_return_details
    def setMembersNode(self, node):
        self.childArray = []
        self.state = State()
        self.state.setMembersState(node.getState())
        if(node.getParent() != None):
            self.parent = node.getParent()
        tempChildArray = node.getChildArray()
        for i in range(len(tempChildArray)):
            tempNode = Node()
            print("setMembersNode")
            tempNode.setMembersNode(tempChildArray[i])
            self.childArray.append(tempNode)

    def setMembersState(self, state):
        self.state = state
        self.childArray = []
    
    def setMembersStatePlus(self, state, parent, childArray):
        self.state = state
        self.parent = parent
        self.childArray = childArray

class Tree:

    def __init__(self):
        self.root = Node()

    def getRoot(self):
        return self.root

    def setRoot(self, root):
        self.root = root

    def addChild(self, parent, child):
        print("before ", len(parent.getChildArray()))
        parent.getChildArray().append(child)
        print("after ", len(parent.getChildArray()))

    def setMembersRoot(self, root):
        self.root = root 

class MonteCarloTreeSearch:
   
    WIN_SCORE = 10 
    def __init__(self):
        self.level = 3

    def getLevel(self):
        return level

    def setLevel(self, level):
        self.level = level

    def getMillisForCurrentLevel(self):
        return 2 * (self.level - 1) + 1

    @show_call_and_return_details
    def findNextMove(self, board, playerNo):
        dt = datetime.now()
        start = dt.microsecond 
        end = start + 2000 * self.getMillisForCurrentLevel()
        #end = start + 20000* self.getMillisForCurrentLevel()
        
        self.opponent = 3 - playerNo
        tree = Tree()
        rootNode = tree.getRoot()
        rootNode.getState().setBoard(board)
        rootNode.getState().setPlayerNo(self.opponent)
        dt = datetime.now()
        iter_start = 0
        iter_end = 20000
        #while ((dt.microsecond) < end):
        while (iter_start < iter_end):
            promisingNode = self.selectPromisingNode(rootNode)
            
            status = promisingNode.getState().getBoard().checkStatus()
            if(status == Board.IN_PROGRESS):
                self.expandNode(promisingNode)
            nodeToExplore = promisingNode
            if(len(promisingNode.getChildArray()) > 0):
                nodeToExplore = promisingNode.getRandomChildNode()
            playoutResult = self.simulateRandomPlayout(nodeToExplore)
            self.backPropogation(nodeToExplore, playoutResult)
         #   dt = datetime.now()
            
            iter_start += 1

        winnerNode = rootNode.getChildWithMaxScore() 
        tree.setRoot(winnerNode)

        return winnerNode.getState().getBoard()

    @show_call_and_return_details
    def selectPromisingNode(self, rootNode):
        node = rootNode
        while(len(node.getChildArray()) != 0):
            node = UCT.findBestNodeWithUCT(node)
        return node

    @show_call_and_return_details
    def expandNode(self, node):
        possibleStates = node.getState().getAllPossibleStates()
        for i in range(len(possibleStates)):
            newNode = Node()
            newNode.setMembersState(possibleStates[i])
            newNode.setParent(node)
            newNode.getState().setPlayerNo(node.getState().getOpponent())
            node.getChildArray().append(newNode)


    @show_call_and_return_details
    def backPropogation(self, nodeToExplore, playerNo):
        tempNode = nodeToExplore
        while( tempNode != None):
            tempNode.getState().incrementVisit()
            if(tempNode.getState().getPlayerNo() == playerNo):
                tempNode.getState().addScore(self.WIN_SCORE)
            tempNode = tempNode.getParent()

    @show_call_and_return_details
    def simulateRandomPlayout(self, node):
        tempNode = Node()
        tempNode.setMembersNode(node)
        tempState = tempNode.getState()
        boardStatus = tempState.getBoard().checkStatus()

        if(boardStatus == self.opponent):
            tempNode.getParent().getState().setWinScore(INTEGER_MIN_VALUE)
            return boardStatus
        while(boardStatus == Board.IN_PROGRESS):
            tempState.togglePlayer()
            tempState.randomPlay()
            boardStatus = tempState.getBoard().checkStatus()
        return boardStatus


class UCT:
    def uctValue(totalVisit, nodeWinScore, nodeVisit):
        if(nodeVisit == 0):
            return INTEGER_MAX_VALUE
        uct = (nodeWinScore / (nodeVisit * 1.0)) + (1.41 * math.sqrt(math.log(totalVisit) / (nodeVisit * 1.0)))
        return uct
    
    @show_call_and_return_details
    def findBestNodeWithUCT(node):
        parentVisit = node.getState().getVisitCount()
        arr = [UCT.uctValue(parentVisit, x.getState().getWinScore(), x.getState().getVisitCount()) for x in node.getChildArray()]
        if(len(arr) == 0):
            print("None in findBestNodeWithUCT")
            return None
        else:
            return node.getChildArray()[arr.index(max(arr))] 
    
        findBestNodeWithUCT = staticmethod(findBestNodeWithUCT)            


class MCTSUnitTest:
    
    def __init__(self):
        self.gameTree = Tree()
        mcts = MonteCarloTreeSearch()

    def test1(self):
        uctValue = 15.79
        print("calc uctValue = ", UCT.uctValue(600, 300, 20))
       
    def test2(self):
        initState = self.gameTree.getRoot().getState()
        possibleStates = initState.getAllPossibleStates()
        if(len(possibleStates) > 0):
            print("test2 pass: posStates len > 0")

    def test3(self):
        board = Board()
        initAvailablePositions = len(board.getEmptyPositions()) 
        board.performMove(Board.P1, Position(1, 1))
        availablePositions = len(board.getEmptyPositions())
        if(initAvailablePositions > availablePositions):
            print("test3 pass")

mcts = MonteCarloTreeSearch()
board = Board()

player = Board.P1
totalMoves = Board.DEFAULT_BOARD_SIZE * Board.DEFAULT_BOARD_SIZE
for i in range(totalMoves):
    board.printBoard()
    board = mcts.findNextMove(board, player)
    if(board.checkStatus() != Board.IN_PROGRESS):
        break;
    player = 3 - player

    winStatus = board.checkStatus()
    
    if(winStatus == Board.DRAW):
        print("Game Drawn")


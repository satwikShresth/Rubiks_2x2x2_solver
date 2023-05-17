from Cube import Cube
from Node import Node
import heapq,json
import time


MAX = float('inf')

class SearchTree:
    def __init__(self, state=None,moves=None,shuffle=None):
        self.cube:Cube
        if state != None:
            self.cube = Cube(state)
        else:
            self.cube = Cube()

        self.recMoves:list
        if moves is not None:
            self.cube.applyMovesStr(moves)

        if shuffle is not None:
            self.cube.shuffle(shuffle)

        self.moveHeuristic = {
            "U":["D'","D","U'"],
            "U'":["D","D'","U"], 
            "R":["L'","L","R'"],
            "R'":["L'","L","R"],
            "F":["B'","B","F'"],
            "F'":["B'","B","F"],
            "D":["U","U'","D'"],
            "D'":["U","U'","D"],
            "L":["R'","R","L'"],
            "L'":["R'","R","L"],
            "B":["F'","F","B'"],
            "B'":["F'","F","B"],
        }
        self.corners = [[8,2,17],[9,3,4],[11,6,13],[10,19,12],[21,0,16],[20,1,5],[23,18,14],[22,7,15]]
        self.cornerIdx:int

    def createRecMoves(self,node:Node):
        self.recMoves= self.cube.moves.copy()
        if len(node) > 0:
            lastMove  = node[-1]
            rm = self.moveHeuristic[lastMove]
            for i in rm:
                self.recMoves.remove(i)
            if len(node) >= 2 and lastMove == node[-2] :
                self.recMoves.remove(lastMove)

    def startNode(self):
        return Node(self.cube.clone())
    
    def printMoveSequence(self,node:Node|bool,time):
        if node:
            printStates = [self.cube.currState]
            print("Move sequence: "," ".join(list(node)))
            for i in node:
                self.cube.applyMove(i)
                printStates.append(self.cube.currState)
            self.cube.print(printStates)
        else:
            print(f"Failed To Find A Solution")
        print(f"Nodes explored :{self.iteration} | Time :{time:.4f}")

    def astar(self):
        node:Node =  self.startNode()
        open = [node]
        startTime = time.time()
        closed = {}
        self.iteration = 0
        while open:
            node = heapq.heappop(open)
            self.iteration+=1
            if node: 
                self.printMoveSequence(node,time.time()-startTime)
                return
            closed[node]=True
            self.createRecMoves(node)
            for move in self.recMoves:
                newNode:Node = node.createChildNode(move) 
                newNode.cost = self.calculateDistance(newNode)
                if str(newNode) not in closed:
                    heapq.heappush(open,newNode)

        return None
    
    def calculateDistance(self,node:Node):
        distance = 0

        for solvedCorner in self.corners:
            state = node.currNodeValue
            solvedState = self.cube.solvedState

            solvedCornerColors = [solvedState[solvedCorner[0]], solvedState[solvedCorner[1]], solvedState[solvedCorner[2]]]
            solvedCornerColors.sort()

            
            for corner in self.corners:
                cornerColors = [state[corner[0]], state[corner[1]], state[corner[2]]]
                cornerColors.sort()
                if cornerColors == solvedCornerColors:
                    distance +=  abs(state.index(cornerColors[0]) - solvedState.index(solvedCornerColors[0])) + abs(state.index(cornerColors[1]) - solvedState.index(solvedCornerColors[1])) + abs(state.index(cornerColors[2]) - solvedState.index(solvedCornerColors[2]))
                    break

        return len(node)+1+(distance//4)
    
    def calculateCost(self,node:Node):
        cost = self.calculateDistance(node)
        cube = Cube(str(node))
        cube.normalize()
        if str(cube.stateString) in self.HeuristicData:
            return len(node)+1+(self.HeuristicData[cube.stateString])
        return cost

    def loadHeuristic(self):
        with open('trainedHeuristicValues.json', 'r') as f:
            self.HeuristicData = json.load(f)
    

    def compAstar(self):
        self.loadHeuristic()
        node:Node =  self.startNode()
        node.cost = self.calculateCost(node)
        open = [node]
        startTime = time.time()
        closed = {}
        self.iteration = 0
        while open:
            node = heapq.heappop(open)
            self.iteration+=1
            if node: 
                self.printMoveSequence(node,time.time()-startTime)
                return
            self.createRecMoves(node)
            for move in self.recMoves:
                newNode:Node = node.createChildNode(move)
                newNode.cost = self.calculateCost(newNode)
                if str(newNode) not in closed:
                    heapq.heappush(open,newNode)
        print()


        N = open.pop(0)
        self.printMoveSequence(N,time.time()-startTime) 
        

    def bfs(self):
        node =  self.startNode()
        open = [node]
        closed = {}
        startTime = time.time()
        self.iteration = 0
        while open:
            N = open.pop(0)
            self.iteration+=1
            if N:
                self.printMoveSequence(N,time.time()-startTime)
                return
            closed[node]=True
            self.createRecMoves(N)
            for move in self.recMoves:
                newNode = N.createChildNode(move)
                if str(newNode) not in closed:
                    open.append(newNode)

        N = open.pop(0)
        self.printMoveSequence(N,time.time()-startTime)  


    def dfs(self,node:Node,depth):
        if depth >= 0:
            self.iteration += 1
            if node:
                return node
            
            self.createRecMoves(node)
            for move in self.recMoves:
                node2 = self.dfs(node.createChildNode(move),depth-1)
                if node2:
                    return node2
        else:
            return False
                

    def dls(self,depth):
        self.iteration =0
        startTime = time.time()
        node = self.dfs(self.startNode(),depth)
        endTime = time.time()
        self.printMoveSequence(node,endTime-startTime)
    

    def idsHelper(self,node:Node,depth):
        self.nodeByDepth = []
        for i in range(depth):
            self.iteration = 0
            node2 = self.dfs(node,i)
            self.nodeByDepth.append(self.iteration-1)
            if node2:
                return node2
        return False

    def ids(self,depth):
        startTime = time.time()
        node = self.idsHelper(self.startNode(),depth)
        endTime = time.time()
        solD = 0
        for idx, itr in enumerate(self.nodeByDepth):
            print(f"Depth: {idx} d: {itr}")
            solD = idx
        print(f"IDS found a solution at depth {solD}")
        self.printMoveSequence(node,endTime-startTime)
        
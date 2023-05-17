from Cube import Cube

class Node:
    def __init__(self,cube:Cube,moves=None):
        self.currNodeValue = cube.stateString
        self.allMoves = cube.moves.copy()
        self.index = 0
        self.solvedState = cube.solvedState
        if isinstance(moves,list):
            self.oldMoves = moves.copy()
        elif moves is not None:
            self.oldMoves = [moves]
        else:
            self.oldMoves = []
        self.cost:int

        
    def createChildNode(self,move):
        cube = Cube(self.currNodeValue)
        cube.applyMove(move)
        newMoveList = self.oldMoves + [move]

        return Node(cube,newMoveList)
    
    def __str__(self):
        return self.currNodeValue
    
    def __len__(self):
        return len(self.oldMoves)
    
    def __getitem__(self, index):
        return self.oldMoves[index]
    
    def __bool__(self):
        cube = Cube(self.currNodeValue)
        return cube.isSolvedQuick()
    
    def __lt__(self, other):
        return self.cost < other

    def __gt__(self, other):
        return self.cost > other

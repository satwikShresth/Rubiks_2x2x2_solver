import sys
from Cube import Cube
from SearchTree import SearchTree
from TrainHeuristic import TrainHeuristic

def printFunction(state=None):
  if state==None:
    Cube().print()
  else:
    Cube(state).print()

def goalFunction(state):
  if Cube(str(state)).isSolved():
    print(True)
  else:
    print(False)

def applyMoveStrFunction(moveSeq,initalState):
  c = Cube(initalState)
  c.applyMovesStr(str(moveSeq))
  c.print()
  
def shuffleFunction(n):
  Cube().shuffle(int(n))

def getSearchTree(moveSeq):
  return SearchTree(moves=moveSeq)

def bfsFunction(moveSeq):
  st:SearchTree=getSearchTree(moveSeq)
  st.bfs()

def testBfsFunction(shuffle):
  st:SearchTree=SearchTree(shuffle=int(shuffle))
  st.bfs()

def dlsFunction(moveSeq,depth):
  st:SearchTree=getSearchTree(moveSeq)
  st.dls(int(depth))

def testDlsFunction(shuffle,depth):
  st:SearchTree=SearchTree(shuffle=int(shuffle))
  st.dls(int(depth))

def idsFunction(moveSeq,depth):
  st:SearchTree=getSearchTree(moveSeq)
  st.ids(int(depth))

def testIdsFunction(shuffle,depth):
  st:SearchTree=SearchTree(shuffle=int(shuffle))
  st.ids(int(depth))

def astarFunction(moveSeq):
  st:SearchTree=getSearchTree(moveSeq)
  st.astar()

def testAstarFunction(shuffle):
  st:SearchTree=SearchTree(shuffle=int(shuffle))
  st.astar()

def competitionFunction(moveSeq):
  st:SearchTree=getSearchTree(moveSeq)
  st.compAstar()

def testCompetitionFunction(shuffle):
  st:SearchTree=SearchTree(shuffle=int(shuffle))
  st.compAstar()

def trainHeuristic():
    th = TrainHeuristic()
    time = th.heuristicDeveloper()
    print('')
    print("Time Taken :",time)

def normFunction(state):
  moveLst = []
  cube = Cube(state)
  print(cube.stateString)
  print("State :",state)
  print()
  print("  Current    "+" "+" Normalized  ")
  print("-"*12+"  "+"-"*13)
  moveLst.append(cube.currState)
  cube.normalize()
  moveLst.append(cube.currState)
  cube.print(cubes=moveLst)


def switchCase(case):
    switcher = {
        "print": printFunction,
        "goal": goalFunction,
        "applyMoveStr": applyMoveStrFunction,
        "shuffle":shuffleFunction,
        "bfs":bfsFunction,
        "ids":idsFunction,
        "dls":dlsFunction,
        "astar":astarFunction,
        "competition":competitionFunction,
        "testBfs":testBfsFunction,
        "testIds":testIdsFunction,
        "testDls":testDlsFunction,
        "testAstar":testAstarFunction,
        "testComp":testCompetitionFunction,
        "train":trainHeuristic,
        "norm":normFunction
    }
    func = switcher.get(case, lambda: "Invalid case")
    return func


def main():
  args = len(sys.argv) - 1
  if args > 0:
    function = switchCase(sys.argv[1])
  
  if args == 1:
    function()
  elif args == 2:
    function(sys.argv[2])
  elif args == 3:
    function(sys.argv[2],sys.argv[3])
  elif args == 4:
    function(sys.argv[2],sys.argv[3],sys.argv[4])

if __name__ == "__main__":
  main()
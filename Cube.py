import random
import sys
import time
import sys

MOVES = {
    "U": [2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23],
    "U'": [1,  3,  0,  2,  8,  9,  6,  7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19,  4,  5, 22, 23],
    "R": [0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23],
    "R'": [0, 22,  2, 20,  5,  7,  4,  6,  8,  1, 10,  3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
    "F": [0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9, 6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
    "F'": [0,  1,  4,  6, 13,  5, 12,  7,  9, 11,  8, 10, 17, 19, 14, 15, 16,  3, 18,  2, 20, 21, 22, 23],
    "D": [0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7],
    "D'": [0,  1,  2,  3,  4,  5, 22, 23,  8,  9,  6,  7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
    "L": [23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
    "L'": [8,  1, 10,  3,  4,  5,  6,  7, 12,  9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20,  2, 22,  0],
    "B": [5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21],
    "B'": [18, 16,  2,  3,  4,  0,  6,  1,  8,  9, 10, 11, 12, 13,  7,  5, 14, 17, 15, 19, 21, 23, 20, 22],
}

class Cube:

  def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
    self.stateString = string.replace(" ", "")
    self.solvedStateString="WWWWRRRRGGGGYYYYOOOOBBBB"
    self.solvedState=[i for i in self.solvedStateString]
    self.moves=[ "U", "U'", "R" , "R'", "F" , "F'", "D" , "D'", "L" , "L'", "B" , "B'"]
    self.currState = [i for i in self.stateString]
    self.fixedPair={0:"U D'",1:"R L'",2:"D U'",3:"F B'",4:"L R'",5:"B F'"}

  def createStateList(self,state):
    return [[char for char in state[i:i+4]] for i in range(0, len(''.join(state)), 4)]

  def norm(self,fixedPoint):
    self.applyMovesStr(self.fixedPair[fixedPoint])

  def normalize(self):
    for j in range(4):
      for k in range(4):
          self.norm(0)
          if [self.stateString[10],self.stateString[12],self.stateString[19]] == ["G","Y","O"]:
            return True
      self.norm(3)
    self.norm(1)
    for j in range(2):
        for k in range(4):
            self.norm(0)
            if [self.stateString[10],self.stateString[12],self.stateString[19]] == ["G","Y","O"]:
              return True
        self.norm(1)
        self.norm(1)
    return False

  def equals(self, cube=None):
    if cube==None:
      cube = self
    checkCube:Cube = self.clone(state=self.solvedState)
    for j in range(4):
      for k in range(4):
          checkCube.norm(0)
          if cube.stateString == checkCube.stateString:
            return True
      checkCube.norm(3)
    checkCube.norm(1)
    for j in range(2):
        for k in range(4):
            checkCube.norm(0)
            if cube.stateString == checkCube.stateString:
              return True
        checkCube.norm(1)
        checkCube.norm(1)
    return False

  def clone(self,state=None):
    if state==None:
      state=self.currState
    
    clone = ''
    for i in range(0, len(state), 4):
      clone+=''.join(state[i:i+4]) + " "

    return Cube(clone)

    # apply a move to a state
  def applyMove(self, move):
    newState = []
    if move in MOVES:
      for colorIdx in MOVES[move]:
        newState.append(self.currState[colorIdx])

    self.currState = newState
    self.stateString = ''.join(self.currState)

    # apply a string sequence of moves to a state
  def applyMovesStr(self, alg:str):
    seq = alg.split()
    for i in seq:
      self.applyMove(i)
    

  def isSolved(self):
    if self.isSolvedQuick():
      return self.equals()
    return False
  
  def isSolvedQuick(self):
    lst = self.createStateList(self.currState)
    for i in lst:
      if len(set(i)) != 1:
        return False
    return True
  
  def shuffle(self, n):
    moveHistory = []
    for _ in range(n):
      randomNumber = random.randint(0, len(self.moves)-1)
      move = self.moves[randomNumber]
      self.applyMove(move)
      moveHistory.append(move)
    print("Shuffled Move Seq:",' '.join(moveHistory))


  def printHelper(self,cubes):
    printHelperList=[]
    remainder = len(cubes)%3
    if remainder != 0:
      printHelperList.append([self.createStateList(cube) for cube in cubes[-remainder:]])
      cubes = cubes[:-remainder]
    for idx, lstIdx in enumerate(range(0,len(cubes),3)):
      addLst = [self.createStateList(cube) for cube in cubes[lstIdx:lstIdx+3]]
      printHelperList.insert(idx,addLst)
    return printHelperList 

  def print(self,cubes = None):
    if cubes==None:
      listCubes = [[self.createStateList(self.currState)]]
    else:
      newLst = []
      listCubes = self.printHelper(cubes)
      print(end="\n")
      # print("-"*13+"-"*14*(len(listCubes[0])-1)+"|")
    for idxLst, lst in enumerate(listCubes):
      length = len(lst)
      for idx in range(length):
        print(f"    {lst[idx][0][0]}{lst[idx][0][1]}",end="        ")
      print(end="\n")
      for idx in range(length):
        print(f"    {lst[idx][0][2]}{lst[idx][0][3]}",end="        ")
      print(end="\n")
      for idx in range(length):
        print(f" {lst[idx][4][0]}{lst[idx][4][1]} {lst[idx][2][0]}{lst[idx][2][1]} {lst[idx][1][0]}{lst[idx][1][1]} {lst[idx][5][0]}{lst[idx][5][1]}",end="  ")
      print(end="\n")
      for idx in range(length):
        print(f" {lst[idx][4][2]}{lst[idx][4][3]} {lst[idx][2][2]}{lst[idx][2][3]} {lst[idx][1][2]}{lst[idx][1][3]} {lst[idx][5][2]}{lst[idx][5][3]}",end="  ")
      print(end="\n")
      for idx in range(length):
        print(f"    {lst[idx][3][0]}{lst[idx][3][1]}",end="        ")
      print(end="\n")
      for idx in range(length):
        print(f"    {lst[idx][3][2]}{lst[idx][3][3]}",end="        ")
      print(end="\n\n")
      # if length > 1:
      #   for idx in range(length-1):
      #     if idxLst is not len(listCubes)-1 and idx >= len(listCubes[idxLst+1]):
      #       print("-"*13,end="-")
      #     else:
      #       print("-"*13,end="+")
      # print("-"*13+"|")
from pulp import *
import math

# currently only solves specific types of sudoku puzzles - the grids must be
# square.
def solveSudoku(sudokuRows,gridSize):
   # make the size of the board whatever size is passed in, the values should
   # be the same size as row/column sizes
   entries = [str(i) for i in range(1,len(sudokuRows)+1)]
   rows = entries
   columns = entries

   # create the board - need to keep structure to add constraints so looks like
   # [[(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)],[(1,4),...]...]
   puzzleBoard = [] 
   for rowMult in range(int(math.sqrt(gridSize))):
      leftGrids = []
      middleGrids = []
      rightGrids = []
      # create left column of grids
      for i in range(3 * rowMult + 1, 3 * (rowMult + 1) + 1):
         for j in range(1,4):
            leftGrids += [(str(i),str(j))]
         for j in range(4,7):
            middleGrids += [(str(i),str(j))]
         for j in range(7,10):
            rightGrids += [(str(i),str(j))]
      puzzleBoard += [leftGrids]
      puzzleBoard += [middleGrids]
      puzzleBoard += [rightGrids]
  
   # set up LP 
   sudokuPuzzle = LpProblem("Sudoku Problem")
   # create dictionary of all the LP variables - keys need to be every
   #combination of (value, row, column) values will be 0 or 1 only (0 if
   #not present - there should be 729 entries (9 ^ 3)
   possibleEntries = LpVariable.dicts("possValue",(entries,rows,columns),0,1,LpInteger)

   # add current puzzle data passed in for constraints 
   for i in range(1,len(sudokuRows)+1):
      curColCount = 0
      currRow = sudokuRows[i]
      for currentEntry in currRow:
         curColCount += 1
         if(currentEntry != '0'):
            sudokuPuzzle += possibleEntries[str(currentEntry)][str(i)][str(curColCount)] == 1
   # sudoku contraints - there can only be one of each value in every row
   # this is the same as saying that if you add the occurences you should
   # get a 1. same goes for column, and individual grids in puzzleBoard 
   for entry in entries:
      # rows constraint
      for row in rows:
         temp = []
         for column in columns:
            temp += possibleEntries[entry][row][column]
         sudokuPuzzle += (lpSum(temp) == 1)
      # columns constraint
      for column in columns:
         temp = []
         for row in rows:
            temp += possibleEntries[entry][row][column]
         sudokuPuzzle += (lpSum(temp) == 1)
      # grid constraint
      for grid in puzzleBoard:
         temp = []
         for (row, column) in grid:
            temp += possibleEntries[entry][row][column]
         sudokuPuzzle += (lpSum(temp) == 1)
 
   for row in rows:
      for column in columns:
         temp = []
         for entry in entries:
            temp += possibleEntries[entry][row][column]
         sudokuPuzzle += (lpSum(temp) == 1)

   sudokuPuzzle.writeLP("sudoku.lp")
   sudokuPuzzle.solve()

   topString = ""
   # they only want the first three values from the first row.
   for column in ["1","2","3"]:
      for entry in entries:
         if value(possibleEntries[entry]["1"][column])==1:
               topString += entry
                
   return topString

if __name__ == "__main__":
   finalSol = 0
   with open("sudoku.txt") as f:
      counter = 0
      currPuzzRows = {}
      # puzzles provided have 9 lines
      numRows = 9
      lines = f.readlines()
      for line in lines:
         # first line in current data format is the "puzzle title", discard
         if counter == 0:
            counter += 1
            continue
         else:
            # take off \n
            currPuzzRows[counter] = line.strip()
            if counter == numRows:
               finalSol += int(solveSudoku(currPuzzRows,numRows))
               counter = 0
            else:
               counter += 1

   print(finalSol)



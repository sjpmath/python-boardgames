import functools
import random

class BoardGame:
  def __init__(self, m, n):
    self.m = m
    self.n = n
    self.board = [['.' for _ in range(n)] for _ in range(m)]

  def print_board(self):
    for line in self.board:
      print(line)
    print("-"*15)

  def get_user_input(self):
    while True:
      userinput = list(input().split(" "))
      try:
        if len(userinput)!=2:
          raise TypeError
        r = userinput[0]; c = userinput[1]
        if (not r.isnumeric()) or (not c.isnumeric()):
          raise TypeError
        else:
          r = int(r); c = int(c)
        if r < 0 or r >= self.m or c < 0 or c >= self.n:
          raise IndexError
      except IndexError:
        print("index out of bounds")
      except TypeError:
        print("please input exactly 2 nonnegative integer values")
      else:
        return (r,c) # return coordinates when the input becomes valid

  def boardcomplete(self):
    for r in range(self.m):
      for c in range(self.n):
        if self.board[r][c]=='.':
          return False
    return True

  @staticmethod
  def func(ch1, ch2):
    if ch1==None:
      return None
    elif ch1 == ch2:
      return ch1

  def rowdone(self, num, r, c, symbol):
    row = []
    for col in range(c, c+num):
      row.append(self.board[r][col])
    win = functools.reduce(BoardGame.func, row, symbol)
    if win:
      return True
    return False

  def coldone(self, num, r, c, symbol):
    col = []
    for row in range(r, r+num):
      col.append(self.board[row][c])
    win = functools.reduce(BoardGame.func, col, symbol)
    if win:
      return True
    return False

  def diag1done(self, num, r, c, symbol):
    diag1 = []
    for d in range(num):
      diag1.append(self.board[r+d][c+d])
    if functools.reduce(BoardGame.func, diag1, symbol):
      return True
  def diag2done(self, num, r, c, symbol):
    diag2 = []
    for d in range(num):
      diag2.append(self.board[r+d][c-d])
    if functools.reduce(BoardGame.func, diag2, symbol):
      return True


class Sudoku(BoardGame):


  @staticmethod
  def valid(board, r, c, n):
    row = {}
    col = {}
    sq = {}
    for c1 in range(9):
      if board[r][c1]!='.': 
        row.update({board[r][c1]: True})
    for r1 in range(9):
      if board[r1][c]!='.': 
        col.update({board[r1][c]: True})
    startr = r//3
    startc = c//3
    for r1 in range(startr, startr+3):
      for c1 in range(startc, startc+3):
        if board[r1][c1]!='.':
          sq.update({board[r1][c1]: True})
    if (n in row) or (n in col) or (n in sq):
      return False
    return True

  @staticmethod
  def generateSudoku():
    validSudoku = [
      ['6', '2', '5', '8', '4', '3', '7', '9', '1'],
      ['7', '9', '1', '2', '6', '5', '4', '8', '3'],
      ['4', '8', '3', '9', '7', '1', '6', '2', '5'],
      ['8', '1', '4', '5', '9', '7', '2', '3', '6'],
      ['2', '3', '6', '1', '8', '4', '9', '5', '7'],
      ['9', '5', '7', '3', '2', '6', '8', '1', '4'],
      ['5', '6', '9', '4', '3', '2', '1', '7', '8'],
      ['3', '4', '2', '7', '1', '8', '5', '6', '9'],
      ['1', '7', '8', '6', '5', '9', '3', '4', '2']
    ]
    # idea: shuffle row and col labels, from existing valid sudoku level
    #only shuffle each group of three to maintain invariant of square rule

    #idea: permutation of rows and permutation of cols uniquely determine grid
    def shuffle(ar): return random.sample(ar, len(ar)) # generate random permutation of ar
    rows = []
    rowperm = shuffle(range(3))
    for r in rowperm:
      perm = shuffle(range(3))
      for p in perm:
        rows.append(r*3+p)
    cols = []
    colperm = shuffle(range(3))
    for c in colperm:
      perm = shuffle(range(3))
      for p in perm:
        cols.append(c*3+p)
    board = [['.' for _ in range(9)] for _ in range(9)]
    for i in range(9):
      for j in range(9):
        board[rows[i]][cols[j]] = validSudoku[i][j]

    return board


  def get_user_input(self):
    while True:
      try:
        r,c = super().get_user_input()
        if self.board[r][c]!='.':
          raise ValueError
        n = input("Enter number to input: ")
        if not n.isnumeric() or int(n) < 1 or int(n) > 9:
          raise AssertionError
      except ValueError:
        print("cell already filled")
      except AssertionError:
        print("please enter integer between 1 and 9")
      else:
        return (r,c,n)



  def __init__(self):
    super().__init__(9,9)
    self.board = Sudoku.generateSudoku()
    xs = random.sample(range(81), 40)
    for x in xs:
      r = int(x/9); c = x%9
      self.board[r][c] = '.'

  def playgame(self):
    rows = [{} for _ in range(9)]
    cols = [{} for _ in range(9)]
    sqs = [[{} for _ in range(3)] for _ in range(3)]
    for r in range(9):
      for c in range(9):
        ro = r//3; co = c//3
        if self.board[r][c]!='.':
          n = self.board[r][c]
          rows[r].update({n:True})
          cols[c].update({n:True})
          sqs[ro][co].update({n:True})

    i = 0
    while i < 41:
      self.print_board()
      r,c,n = self.get_user_input()
      ro = r//3; co = c//3
      if n in rows[r] or n in cols[c] or n in sqs[ro][co]:
        print("violation")
      else:
        self.board[r][c] = n
        rows[r].update({n:True})
        cols[c].update({n:True})
        sqs[ro][co].update({n:True})
        i+=1
    print("finished!")



class MineSweeper(BoardGame):
  def __init__(self):
    super().__init__(9,9)
    xs = random.sample(range(0,81), 40)
    for x in xs:
      r = int(x/9); c = x%9
      self.board[r][c] = 'M'
    self.score = 0
    self.boarddisplay = []
    for line in self.board:
      line1 = line.copy()
      for i in range(len(line1)):
        if line1[i]=='M': line1[i]='.'
      self.boarddisplay.append(line1)

  def print_board(self):
    for line in self.boarddisplay:
      print(line)
    print("-"*15)

  def get_user_input(self):
    while True:
      try:
        r,c = super().get_user_input()
        if self.boarddisplay[r][c]!='.' and self.boarddisplay[r][c]!='M':
          raise ValueError
        t = input("Are you selecting (S) or flagging (F)?")
        if t!='F' and t!='S':
          raise AssertionError
      except ValueError:
        print("cell already revealed/flagged")
      except AssertionError:
        print("enter S or F for type of command")
      else:
        return (r,c,t)

  def playgame(self):
    for i in range(81):
      self.print_board()
      r,c,t = self.get_user_input()
      if self.board[r][c]=='M' and t=='S':
        print("you touched a mine!")
        break
      elif t=='S':
        count = 0
        dr = [1,-1,1,-1,1,-1,0,0]
        dc = [0,0,1,-1,-1,1,1,-1]
        for k in range(8):
          nr = r + dr[k]; nc = c+dc[k]
          if nr<0 or nr>=9 or nc<0 or nc>=9:
            continue
          if self.board[nr][nc]=='M':
            count += 1
        self.board[r][c] = str(count)
        self.boarddisplay[r][c] = str(count)
        self.score += 1
      elif t=='F':
        self.boarddisplay[r][c] = 'F'
      if self.score==41:
        print("you win!")
        break





class Omok(BoardGame):
  def __init__(self):
    super().__init__(15,15)

  def get_user_input(self):
    while True:
      try:
        r,c = super().get_user_input()
        if self.board[r][c]!='.':
          raise ValueError
      except ValueError:
        print("cell already played")
      else:
        return (r,c)

  def hasWon(self, player, symbol, r, c):
    for col in range(max(0, c-4), c+1):
      if col >= 0 and col+4 < 15:
        if super().rowdone(5, r, col, symbol):
          return True
    for row in range(max(0,r-4), r+1):
      if row >= 0 and row+4 < 15:
        if super().coldone(5, row, c, symbol):
          return True
    for d in range(5):
      row = r-d; col = c-d
      if row >= 0 and row+4 < 15 and col >= 0 and col+4 < 15:
        if super().diag1done(5, row, col, symbol):
          return True
      row = r-d; col = c+d
      if row >= 0 and row+4 < 15 and col-4 >= 0 and col < 15:
        if super().diag2done(5, row, col, symbol):
          return True
    return False

  def playgame(self):
    symbol = ['O', 'X']
    for i in range(225):
      super().print_board()
      player = i%2
      r,c = self.get_user_input() #r,c is a valid play
      self.board[r][c] = symbol[player]
      if self.hasWon(0, symbol[0], r, c):
        print("player ", 0, " has won")
        break
      elif self.hasWon(1, symbol[1], r, c):
        print("player ", 1, " has won")
        break
      elif super().boardcomplete():
        print("tied")
        break


class TicTacToe(BoardGame):
  def __init__(self):
    super().__init__(3,3)

  def get_user_input(self):
    while True:
      try:
        r,c = super().get_user_input()
        if self.board[r][c]!='.':
          raise ValueError
      except ValueError:
        print("cell already played")
      else:
        return (r,c)

  def hasWon(self, player, symbol):
    for r in range(3):
      if super().rowdone(3, r, 0, symbol):
        return True
    for c in range(3):
      if super().coldone(3, 0, c, symbol):
        return True
    if super().diag1done(3, 0, 0, symbol):
      return True
    if super().diag2done(3, 0, 2, symbol):
      return True
    return False

  def playgame(self):
    symbol = ['O', 'X']
    for i in range(9):
      super().print_board()
      player = i%2
      r,c = self.get_user_input() #r,c is a valid play
      self.board[r][c] = symbol[player]
      if self.hasWon(0, symbol[0]):
        print("player ", 0, " has won")
        break
      elif self.hasWon(1, symbol[1]):
        print("player ", 1, " has won")
        break
      elif super().boardcomplete():
        print("tied")
        break



"""
class TicTacToe:
  def __init__(self):
    self.board = [
      ['.', '.', '.'],
      ['.', '.', '.'],
      ['.', '.', '.']
    ]
  def print_board(self):
    for line in self.board:
      print(line)
    print("-"*15)

  def play(self, player):
    symbol = ''
    if player==0:
      symbol = '0'
    else:
      symbol = 'X'
    userinput = list(input().split(" "))
    try:
      if len(userinput)!=2:
        raise TypeError
      r = userinput[0]; c = userinput[1];
      if (not r.isnumeric()) or (not c.isnumeric()):
        raise TypeError
      else:
        r = int(r); c = int(c)
      if r < 0 or r > 2 or c < 0 or c > 2:
        raise IndexError
      elif self.board[r][c]=='.':
        self.board[r][c] = symbol
      else:
        raise ValueError
    except IndexError:
      print("index out of bounds")
      return False
    except ValueError:
      print("cell already played")
      return False
    except TypeError:
      print("please input exactly 2 nonnegative integer values")
    else:
      return True

  

  def hasWon(self, player):
    def func(ch1, ch2):
      if ch1==None:
        return None
      elif ch1 == ch2:
        return ch1
    symbol = ''
    if player==0:
      symbol = '0'
    else:
      symbol = 'X'
    for r in range(3):
      row = []
      for c in range(3):
        row.append(self.board[r][c])
      win = functools.reduce(func, row, symbol)
      if win:
        return True
    for c in range(3):
      col = []
      for r in range(3):
        col.append(self.board[r][c])
      win = functools.reduce(func, col, symbol)
      if win:
        return True
    diag1 = []
    for d in range(3):
      diag1.append(self.board[d][d])
    if functools.reduce(func, diag1, symbol):
      return True
    diag2 = []
    for d in range(3):
      diag2.append(self.board[d][2-d])
    if functools.reduce(func, diag2, symbol):
      return True
    return False

  def boardcomplete(self):
    for r in range(3):
      for c in range(3):
        if self.board[r][c]=='.':
          return False
    return True
    
  
  def playgame(self):
    for i in range(9):
      self.print_board()
      validplay = self.play(i%2)
      while not validplay:
        validplay = self.play(i%2)
      if self.hasWon(0):
        print("player ", 0, " has won")
        break
      elif self.hasWon(1):
        print("player ", 1, " has won")
        break
      elif self.boardcomplete():
        print("tied")
        break
"""
        
      

obj = Sudoku()
obj.playgame()
        
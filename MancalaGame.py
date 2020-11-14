import sys  
import numpy as np
from MancalaBoard import MancalaBoard

class MancalaGame:

  def __init__(self, size=6 , beans=4) :
    self.board = MancalaBoard(size)
    self.board.set_beans(beans)
    self.moves = []
    
  def move(self, pit):
    cp = np.copy(self.board.pit)
    b = self.board.pit[pit]
    s = 0
    end_index = -1
    if (pit<=self.board.player_max_index):
      s = (pit+b+self.board.opponent_min_index)//(self.board.opponent_store_index)
      end_index = (b + pit) % (self.board.opponent_max_index+1)
    else:
      s =  (pit+b)//(self.board.opponent_store_index)
      #p = pit - self.board.opponent_min_index
      end_index = ((b+pit - self.board.opponent_min_index) % (self.board.opponent_max_index+1) + self.board.opponent_min_index  ) % (self.board.opponent_store_index+1)
      #end_index = (b + pit) % (self.board.opponent_max_index+1)
    #print ("s: {}").format(s)
    b = b - s
    self.board.pit[pit] = 0
    a = np.zeros(self.board.opponent_max_index, np.int32)
    if (pit<=self.board.player_max_index):
      indices = np.arange(pit+1, pit+b+1, dtype=np.int32)
      np.remainder(indices, self.board.opponent_max_index, indices)
      np.add.at(a, indices, 1)
      a = np.append(a, 0)
      a = np.insert(a, self.board.player_max_index+1, s)
    else:
      indices = np.arange(pit, pit+b, dtype=np.int32)
      np.remainder(indices, self.board.opponent_max_index, indices)
      np.add.at(a, indices, 1)
      a = np.insert(a, self.board.player_max_index+1, 0)
      a = np.append(a, s)
    self.board.pit+=a
    if (self.board.pit[end_index] == 1): #Stealing
      if(pit<self.board.player_store_index and end_index<self.board.player_store_index): #Player stealing
        opp_i = self.board.opponent_min_index+self.board.player_max_index-end_index
        if (self.board.pit[opp_i]>0): #There is something to steal
          self.board.pit[self.board.player_store_index] += self.board.pit[opp_i]+1
          self.board.pit[opp_i] = 0
          self.board.pit[end_index] =0
      elif(pit>self.board.player_store_index and self.board.opponent_store_index>end_index>self.board.player_store_index): #Opponent stealing
        opp_i = self.board.player_max_index - end_index + self.board.opponent_min_index
        if (self.board.pit[opp_i]>0): #There is something to steal
          self.board.pit[self.board.opponent_store_index] += self.board.pit[opp_i]+1
          self.board.pit[opp_i] = 0
          self.board.pit[end_index] =0
    return end_index
  
  def show(self):
    print('{:2d}               {:2d}'.format(self.board.get_opponent_store(), self.board.get_player_store()))
    print('{}'.format(np.stack((np.flipud(self.board.pit[game.board.opponent_min_index:game.board.opponent_max_index+1]), self.board.pit[0:game.board.player_max_index+1]))))
    #print'{}'.format(self.board.pit)
 
  def in_play(self):
    return (self.board.pit[0:game.board.player_max_index+1].any() and self.board.pit[game.board.opponent_min_index:game.board.opponent_max_index+1].any())

  def end_score(self):
    return (np.sum(self.board.pit[0:self.board.opponent_min_index]), np.sum(self.board.pit[self.board.opponent_min_index:self.board.size]))
  
  def player_nonzero_move(self):
    nz=np.flatnonzero(self.board.pit)
    nz=nz[nz<self.board.player_store_index]
    np.random.shuffle(nz)
    return nz[0]
  
  def opponent_nonzero_move(self):
    nz=np.flatnonzero(self.board.pit)
    nz=nz[nz>self.board.player_store_index]
    nz=nz[nz<self.board.opponent_store_index]
    np.random.shuffle(nz)
    return nz[0]

def single_player_game(game):
  #game = MancalaGame()
  player_move=True
  moves = 0
  while(game.in_play()):
    game.show()
    moves+=1
    if (player_move):
      """pla_move_i = game.player_nonzero_move()
      #print ("Players move: {}").format(pla_move_i)
      if (game.move(pla_move_i) != game.board.player_store_index):
        player_move=False
      """
      i = input("Your move: ")
      try:
        i = int(i)
      except ValueError:
        print("Not an integer!")
        continue
      else:
        #print(isinstance(i, (int))
        i-=1
        if (0<=i<=game.board.player_max_index):
          if (game.board.pit[i] != 0):
            if (game.move(i) != game.board.player_store_index): #Check, if move ended in store
              player_move=False
          else:
            print("Empty pit!")
        else:
          print("Wrong index!")
          continue
    else:
      opp_move_i = game.opponent_nonzero_move()
      print("Opponents move: {}".format(opp_move_i))
      if (game.move(opp_move_i) != game.board.opponent_store_index):
        player_move=True
      """i = raw_input("Opponents move: ")
      try:
        i = int(i)
      except ValueError:
        print("Not an integer!")
        continue
      else:
        if (game.board.opponent_min_index<=i<=game.board.opponent_max_index):
          if (game.move(i) != game.board.opponent_store_index):
            player_move=True
        else:
          print("Wrong index!")
          continue"""
  game.show()
  print("Score: {}".format(game.end_score()))
  print("Moves: {}".format(moves))

def zero_player_game(game):
  #game = MancalaGame()
  player_move=True
  moves = 0
  while(game.in_play()):
    #game.show()
    moves+=1
    if (player_move):
      player_move_i = game.player_nonzero_move()
      #print("Players move: {}".format(player_move_i))
      if (game.move(player_move_i) != game.board.player_store_index):
        player_move=False
    else:
      opp_move_i = game.opponent_nonzero_move()
      #print("Opponents move: {}".format(opp_move_i))
      if (game.move(opp_move_i) != game.board.opponent_store_index):
        player_move=True
  #game.show()
  print("Score: {}".format(game.end_score()))
  print("Moves: {}".format(moves))


if __name__ == '__main__':
  for x in range(10):
    game = MancalaGame()
    print("Game {}".format(x))
    zero_player_game(game)

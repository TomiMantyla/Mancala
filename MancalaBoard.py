import numpy as np

class MancalaBoard:

  def __init__(self, halfsize=6):
  #create board 
    self.size = halfsize*2+2
    self.pit = np.zeros(self.size, np.int32)
    self.player_max_index = self.pit.size//2-2
    self.opponent_min_index = self.pit.size//2
    self.opponent_max_index = self.pit.size-2
    self.player_store_index = self.pit.size//2-1
    self.opponent_store_index = self.pit.size-1
    
  def set_beans(self, n=7):
  #Set beans to pits, n is amount of beans per pit.
    self.pit.fill(n)
    self.pit[self.player_max_index+1]=0
    self.pit[self.opponent_store_index]=0
  
  def get_player_store(self):
    return int(self.pit[self.player_store_index])
 
  def get_opponent_store(self):
    return int(self.pit[self.opponent_store_index])

  def get_state(self):
    return np.copy(self.pit)

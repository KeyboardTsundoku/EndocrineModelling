from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

# Alpha hormone
class Alpha(Agent):
  def __init__(self, unique_id):
    self.unique_id = unique_id
    self.value = 1
    
  def step(self, model):
    print("unique id: ", self.unique_id)
    self.value += 1
    self.move(model)

  def move(self, model):
    x, y = self.pos
    width = model.grid.width
    new_position = (0,0)
    if (width <= x+1):
      new_position = (0, y)
    else:
      new_position = (x+1, y)
    
    print("current position is: ", new_position)
    model.grid.move_agent(self, new_position)
    print("success!!!")

# Bloodstream the space in which hormones exist
class Bloodstream(Model):
  def __init__(self, N, width, height):
    self.running = True
    self.num_alphas = N
    self.schedule = RandomActivation(self)
    self.grid = MultiGrid(height, width, True)

    # create alphas
    for i in range(self.num_alphas):
      a = Alpha(i)
      self.schedule.add(a)
      x = 3
      y = 6
      self.grid.place_agent(a, (x,y))

  def step(self):
    self.schedule.step()

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import random

class Source(Agent):
  def __init__(self, id, size):
    self.rate = 1 # means it'll happen at each step, increase to slow rate
    self.time = 0
    self.unique_id = id
    self.low = 30
    self.up = 1
    self.size = size
  
  def step(self, model):
    print("total omega is: ", model.num_omega)
    if model.num_omega >= 0: 
      self.rate = min(model.num_omega / self.size * 100 + 1, 30)
      print("rate of alpha secretion is: ", self.rate)
    else:
      self.rate = self.up
      model.num_omega = 0
    
    if self.time % int(self.rate) == 0:
        self.secreteAlpha(model)

    self.time += 1

  def secreteAlpha(self, model):
    #print("new alpha secreted!")
    a = Alpha(self.time)
    y = random.randrange(model.grid.height)
    model.grid.place_agent(a, (0,y))
    model.schedule.add(a)

# on contact with alpha generate beta at a random rate
class Target(Agent):
  def __init__(self, id):
    self.unique_id = id
    self.binding = 0.2 # rate at which binding occurs
    self.time = 0

  def step(self, model):
    if self.time % self.rate == 0:
      self.secreteOmega(model)
    self.time += 1

  def secreteOmega(self, model):
    print("new omega secreted!")
    o = Omega(self.time)
    y = random.randrange(model.grid.height)
    model.grid.place_agent(o, (model.grid.width-1, y))
    model.schedule.add(o)
    model.num_omega += 1

# Alpha hormone
class Alpha(Agent):
  def __init__(self, unique_id):
    self.unique_id = unique_id
    
  def step(self, model):
    #print("unique id: ", self.unique_id)
    self.move(model)

  def move(self, model):
    x, y = self.pos
      
    if (x+1 < model.grid.width):
      model.grid.move_agent(self, (x+1, y))
    else:
      # randomly bind alpha to target and secrete omega
      if (model.num_omega >= 0 and random.random() <  model.target.binding):
        model.target.secreteOmega(model) 

class Omega(Agent):
  def __init__(self, unique_id):
    self.unique_id = unique_id
    self.life = 5

  def step(self, model):
    #print("unique id: ", self.unique_id)
    if (self.life > 0):
      self.life -= 1
    self.move(model)

  def move(self, model):
    x, y = self.pos
    
    # if life is finished remove from bloodstream
    if (self.life == 0):
      model.grid.move_agent(self, (-1, -1))
      model.num_omega -= 1
    elif (x-1 >=  0):
      model.grid.move_agent(self, (x-1, y))

# Bloodstream the space in which hormones exist
class Bloodstream(Model):
  def __init__(self, N, width, height):
    self.running = True
    self.schedule = BaseScheduler(self)
    self.grid = MultiGrid(height, width, False)
    self.source = Source("source", height * width)
    self.target = Target("target")
    self.schedule.add(self.source)
    self.num_omega = 0
    #self.schedule.add(self.target)


  def step(self):
    self.schedule.step()

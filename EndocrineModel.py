from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import random

# pituitary organ pumps tsh to thyroid which generates t4
# enough t4 reduces pituitary pumping tsh

# tsh hormone
class TSH(Agent):
  # initialise tsh agent
  def __init__(self, unique_id):
    self.unique_id = unique_id

  # step sequence
  def step(self, model):
    x, y = self.pos

    if (x + 1 < model.grid.width):
      model.grid.move_agent(self, (x + 1, y))

# t4 hormone
class T4(Agent):
  # initialise t4 agent
  def __init__(self, unique_id):
    self.unique_id = unique_id

# source organ
class Pituitary(Agent):
  def __init__(self, id):
    self.unique_id = id
    self.stepID = 0 # increment this to store id of hormones THIS BE BAD

  def step(self, model):
    self.secrete(model)
    self.stepID += 1

  # secrete hormones, at this point only tsh
  def secrete(self, model):
    t = TSH(self.stepID)
    y = random.randrange(model.grid.height)
    model.grid.place_agent(t, (0, y))
    model.schedule.add(t)

# target organ
class Thyroid(Agent):
  def __init__(self, id):
    self.unique_id = id

# model
class Bloodstream(Model):
  # initialise source organ
  def __init__(self, N, width, height):
    self.num_agents = N
    self.grid = MultiGrid(height, width, True)
    self.schedule = BaseScheduler(self)
    self.source = Pituitary("Pituitary")
    self.target = Thyroid("Thyroid")
    self.schedule.add(self.source)

  # advance a step
  def step(self):
    self.schedule.step()

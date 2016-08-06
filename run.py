from EndocrineModel import *
import matplotlib.pyplot as plt
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

'''
model = Bloodstream(20, 10, 10)

for i in range(20):
  model.step()
'''

def agent_portrayal(agent):
  portrayal = {
    "Shape": "circle", 
    "Filled": "true", 
    "Layer": 0, 
    "r": 0.5 
  }
  
  if type(agent) is Alpha:
    portrayal["Color"] = "red"
  elif type(agent) is Omega:
    portrayal["Color"] = "blue"

  return portrayal

chart = ChartModule([{
  "Label": "Alpha",
  "Color": "black"}],
  data_collector_name= "datacollector"
)
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(Bloodstream, [grid, chart], "Endocrine Model", 100, 10, 10)
server.port = 8888
server.launch()

'''
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
  cell_content, x, y = cell
  agent_count = len(cell_content)
  agent_counts[y][x] = agent_count

plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()
plt.show()
'''

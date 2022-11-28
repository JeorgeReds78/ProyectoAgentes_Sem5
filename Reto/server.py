from agents import *
from model import Model
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):    
    portrayal = {"Shape": "circle",
                "Filled": True,
                "Layer": 0,
                }

    if type(agent) is Road:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "grey"
    
    if type(agent) is Destination:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9

    if type(agent) is Traffic_Light:
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.25

    if type(agent) is Obstacle:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9

    if type(agent) is Car:
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    return portrayal



with open('d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA/new.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines) - 1
    height = len(lines)

    print(f'width: {width}, height: {height}')

model_params = {"numberCars":1}

grid = CanvasGrid(agent_portrayal, width, height, 400, 400)

server = ModularServer(Model, [grid], "Traffic Simulation", model_params)

server.port = 8521 # The default
server.launch()
"""
    Server instanciated on Mesa for the simulation.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 22/11/2022
    Last Modification: 2/12/2022
"""

from agents import * # Import Car, Road, Traffic_Light, Obstacle and Destination agents
from model import Model # Import Model class
from mesa.visualization.modules import CanvasGrid # Import CanvasGrid module
from mesa.visualization.ModularVisualization import ModularServer # Import ModularServer class
from mesa.visualization.UserParam import UserSettableParameter # Import UserSettableParameter class

def agent_portrayal(agent):
    """ Function to portray agents.
    
            Parameters:
                - agent : Agent to be portrayed
    
            Returns:
                - portrayal : Dictionary with portrayal information
        """
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

with open('d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA2.4/python/new.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines) - 1
    height = len(lines)

    print(f'width: {width}, height: {height}')

model_params = {"numberCars": UserSettableParameter(
    "slider", 
    "Number of cars", 
    4, # DEFAULT VALUE
    1, # Min value
    10, # Max value
    1
    ),}

grid = CanvasGrid(agent_portrayal, width, height, 400, 400)

server = ModularServer(Model, [grid], "Traffic Simulation", model_params)

server.port = 8521 # The default
server.launch()
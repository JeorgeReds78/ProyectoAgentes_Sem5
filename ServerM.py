"""
    Server for the "Integradora project" on mesa.ModularServer side

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 16/11/2022
    Last Modification: 21/11/2022
"""

# Imports 
from mesa.visualization.modules import CanvasGrid # CanvasGrid is a visualization module that displays a grid of cells
from mesa.visualization.ModularVisualization import ModularServer # ModularServer is a class that allows
from mesa.visualization.UserParam import UserSettableParameter # Lets user decide the parameters of the model


from Modelo import ModelClass # Import the class ModelClass
from mesa.visualization.modules import CanvasGrid # CanvasGrid is a visualization module that displays a grid of cells

from Agentes import Bot, Box # Import the class Bot and Box

# Constants
NUMBER_OF_CELLS = 10
SIZE_OF_CANVAS_IN_PIXELS_X = 800
SIZE_OF_CANVAS_IN_PIXELS_Y = 800
PORT = 8080

# Create a grid of 10x10 cells and 10 boxes
simulation_params = {
    "numberOfBoxes": 10,
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
    "steps": UserSettableParameter(
        "slider", 
        "Steps", 
        1250, # Default 
        100, # Min
        10000, # Max
        1 # Step
    ),
}

def agent_portrayal(agent):
    """ Portrayal of the agents.

    Args:
        agent (Agent): Agent to portray.

    Returns:
        portrayal (dict): Dictionary with the portrayal of the agent.
    """
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    if type(agent) is Bot and agent.hasBox == False:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 0,
            "Color": "blue",
        }
    elif type(agent) is Bot and agent.hasBox == True:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 0,
            "Color": "red",
        }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.2,
            "Layer": 0,
            "Color": "brown",
        }
    return portrayal

# Create a canvas grid
grid = CanvasGrid(agent_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

# Create a server
server = ModularServer(ModelClass, [grid], "Bots", simulation_params)
server.port = PORT # Server port
server.launch() # Launch the server
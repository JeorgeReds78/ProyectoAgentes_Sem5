"""
    Server initialization with RoombaModel from Modelo.py
    Using the server_portrayal function to show the agents
    Stablishing UserSettableParameters to change the number of Roombas,Trashes and Timer.


    Authors:
        - Carlos Alan Gallegos Espindola (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)

    Date of creation: 10/11/2022
    Last Modification: 11/11/2022
"""

# Imports
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Modelo import ModeloRoomba
from mesa.visualization.modules import CanvasGrid, ChartModule

# Constants
NUMBER_OF_CELLS = 10
SIZE_OF_CANVAS_IN_PIXELS_X = 800
SIZE_OF_CANVAS_IN_PIXELS_Y = 800
PORT = 8080

simulation_params = {
    "numberOfAgents" : UserSettableParameter(
        "slider",
        "Number of Roombas",
        1, # Default
        1, # Min
        20, # Max
        1, # Step
        description = "Choose how many Roombas to include in the simulation"
    ),
    "numberOfTrashes" : UserSettableParameter(
        "slider",
        "Number of Trashes",
        10, # Default
        5, # Min
        50, # Max
        1, # Step
        description = "Choose how many Trashes to include in the simulation"
    ),
    "seconds" : UserSettableParameter(
        "slider",
        "Run time",
        15, # Default
        10, # Min
        120, # Max
        1, # Step
        description = "Choose how much time to run the simulation"
    ),

    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS
}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    if agent.type == "Roomba":
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 0,
            "Color": "green",
        }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "r": 0.5,
            "Layer": 0,
            "Color": "red",
        }
    return portrayal

chartCurrents = ChartModule(
    [
        {"Label": "Trashes", "Color": "red"},
        {"Label": "Time", "Color": "blue"},
    ],
    canvas_height = 300,
    data_collector_name = "datacollector_currents"
)

grid = CanvasGrid(agent_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

server = ModularServer(ModeloRoomba, [grid, chartCurrents], "Roomba", simulation_params)
server.port = PORT
server.launch()
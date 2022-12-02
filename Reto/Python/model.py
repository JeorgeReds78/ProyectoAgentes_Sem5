"""
    Model class for the simulation.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 22/11/2022
    Last Modification: 2/12/2022
"""

from mesa import Model # Base class for all models
from mesa.time import RandomActivation # Scheduler to activate agents
from mesa.space import MultiGrid # Grid where agents are placed
from agents import * # Import Car, Road, Traffic_Light, Obstacle and Destination agents
import json # To read json files

class Model(Model):
    """ Model class for simulation.

        Methods:
            - __init__ : Constructor
            - step : Advance the model by one step
    """

    def __init__(self, numberCars = 4):
        """ Constructor for Model class.

            Parameters:
                - numberCars : Number of cars to be created

            Returns:
                - None
        """
        super().__init__(self, numberCars)

        dataDictionary = json.load(open("d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA2.3/python/mapDictionary.json"))

        self.traffic_lights = []

        with open('d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA2.4/python/new.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines)-1
            self.height = len(lines)
            print(self.width, self.height)
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            self.numberCars = numberCars
            self.running = True
            self.destinations = []
            roadsList = []

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        if col == "v":
                            roadMap = Road(f"r_{r*self.width+c}", self, "south")
                            self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        elif col == "^":
                            roadMap = Road(f"r_{r*self.width+c}", self, "north")
                            self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        elif col == ">":
                            roadMap = Road(f"r_{r*self.width+c}", self, "east")
                            self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        elif col == "<":
                            roadMap = Road(f"r_{r*self.width+c}", self, "west")
                            self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        roadsList.append((c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        roadMap = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        self.schedule.add(roadMap)
                        self.traffic_lights.append(roadMap)

                    elif col == "#":
                        roadMap = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(roadMap, (c, self.height - r - 1))

                    elif col == "D":
                        roadMap = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(roadMap, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))

            for i in range(self.numberCars):
                agent = Car(1000 + i, self, self.destinations[self.random.choice(range(13))]) # create car agent with id, model, destination
                carPos = self.random.choice(roadsList) # give car random road position
                self.grid.place_agent(agent, carPos) # place agent in grid
                self.schedule.add(agent) # add agent to schedule

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
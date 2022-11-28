from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import *
import json

class Model(Model):

    def __init__(self, numberCars):
        super().__init__(self, numberCars)

        dataDictionary = json.load(open("d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA/mapDictionary.json"))

        self.traffic_lights = []

        with open('d:/Storage/ThisPC/Storage/Git/Examen/CODIGOLUNA/new.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines)-1
            self.height = len(lines)
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            self.num_agents = numberCars
            self.running = True
            self.destinations = []

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

            #for i in range(self.num_agents):
            car = Car(1000, self,self.random.choice(self.destinations))
            self.schedule.add(car)
            self.grid.place_agent(car, (0, 0))
            car = Car(1001, self,self.random.choice(self.destinations))
            self.schedule.add(car)
            self.grid.place_agent(car, (0, 24))
            car = Car(1002, self,self.random.choice(self.destinations))
            self.schedule.add(car)
            self.grid.place_agent(car, (23, 0))
            car = Car(1003, self,self.random.choice(self.destinations))
            self.schedule.add(car)
            self.grid.place_agent(car, (23, 24))
            car = Car(1004, self,self.random.choice(self.destinations))
            self.schedule.add(car)
            self.grid.place_agent(car, (1, 0))

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
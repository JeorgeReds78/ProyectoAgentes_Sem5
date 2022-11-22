"""
    Model class for the Integradora project.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 16/11/2022
    Last Modification: 21/11/2022
"""

# Imports
from mesa import Model # Model is the base class for all models in Mesa
from Agentes import Bot, Box # Import the class Bot and Box
from mesa.time import RandomActivation  # RandomActivation is a scheduler that activates each agent once per step, in random order, with the order reshuffled every step.
from mesa.space import MultiGrid # MultiGrid is a grid that allows multiple objects to occupy the same cell.

class ModelClass(Model):
    ''' Class that represents the model

        Methods:
            - __init__: Constructor of the class
            - step: Method that makes the model move
            - createAgents: Method that creates the agents
    '''

    def __init__(self, numberOfBoxes, width, height):
        ''' Constructor of the class

            Args:
                - self: Instance of the class
                - numberOfBoxes: Number of boxes in the model
                - width: Width of the model
                - height: Height of the model

            Returns:
                - None
        '''
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.num_boxes = numberOfBoxes
        spaces = self.grid.width * self.grid.height
        rspaces = list(range(spaces))
        rspaces.remove(0)
        rspaces.remove(1)
        rspaces.remove(2)
        rspaces.remove(3)
        rspaces.remove(4)

        # ?Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Create Bots
        for i in range(5):
            a = Bot(i, self,False,self.num_boxes)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            place = self.random.choice(rspaces)
            rspaces.remove(place)
            place = [int(x) for x in str(place)]
            if len (place) == 1:
                x = int(place[0])
                y = int(place[0])
            elif len (place) == 2:
                x = int(place[0])
                y = int(place[1])
            elif len (place) == 3:
                x = int(place[0],place[1])
                y = int(place[3])
            elif len (place) == 4:
                x = int(place[0],place[1])
                y = int(place[3],place[4]), (x, y)

        # Create Boxes
        for i in range(6, 6+numberOfBoxes):
            b = Box(i, self,False,False,True)
            self.schedule.add(b)
            # Add the agent to a random grid cell
            place = self.random.choice(rspaces)
            rspaces.remove(place)
            place = [int(x) for x in str(place)]
            if len (place) == 1:
                x = int(place[0])
                y = int(place[0])
            elif len (place) == 2:
                x = int(place[0])
                y = int(place[1])
            elif len (place) == 3:
                x = int(place[0],place[1])
                y = int(place[3])
            elif len (place) == 4:
                x = int(place[0],place[1])
                y = int(place[3],place[4])
            self.grid.place_agent(b, (x, y))

    def step(self):
        ''' Method that makes the model move

            Args:
                - self: Instance of the class

            Returns:
                - None
        '''
        self.schedule.step()
        if self.current_boxes_stacked(self):
            self.running = False

    @staticmethod
    def current_boxes_stacked(model):
        ''' Method that checks if the boxes are stacked

            Args:
                - self: Instance of the class

            Returns:
                - True if the boxes are stacked (finished)
        '''
        for agent in  model.schedule.agents:
            if type(agent) == Bot:
                if agent.finished:
                    return True 
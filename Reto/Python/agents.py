"""
    Agents class for the Model class.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 22/11/2022
    Last Modification: 2/12/2022
"""

from mesa import Agent # Import the Agent class from the mesa module

class Car(Agent):
    ''' Class that represents the car agent 

        Methods:
            - __init__: Constructor of the class
            - step: Method that is called every step of the model
            - move: Method that moves the car
            - onEdge: Method that checks if the car is on the edge of the grid
            - onBorder: Method that checks if the car is on the border of the grid
            - whatDirImOn: Method that checks the direction of the road the car is on
            - whatDirItIs: Method that checks the direction of the road the car is going to
            - onCorner: Method that checks if the car is on a corner of the grid
            - nearEdge: Method that checks if the car is near the edge of the grid
            - nearBorder: Method that checks if the car is near the border of the grid
    '''
    def __init__(self, unique_id, model, destiny):
        '''Constructor of the Car class
        
            Parameters:
                - unique_id: Unique identifier of the agent
                - model: Model that the agent belongs to
                - destiny: Destiny of the car
                
            Attributes:
                - destiny: Destiny of the car
                - nextPosition: Next position of the car
                - arrived: Boolean that indicates if the car has arrived to its destiny
                - previousPosition: Previous position of the car
                - facing: Direction the car is facing [north, south, east, west]
                - status: Boolean that indicates if the car has crashed [For Unity visualization]
        '''
        super().__init__(unique_id, model)
        self.destiny = destiny # ?  Destination of the car to arrive
        self.nextPosition = None # ?  Next position of the car 
        self.arrived = False
        self.prevPosition = []
        self.facing = None
        self.status = True

    def step(self):
        ''' Method that is called every step of the model

            Args:
                - self: Instance of the class

            Returns:
                - None
        '''
        if not self.arrived or self.status:
            self.move()

    def move(self):
        ''' Method that moves the car to the next position
        
            Args:
                - self: Instance of the class
            
            Returns:
                - None
        '''
        self.currPosiblePositions = self.model.grid.get_neighborhood(self.pos,moore=False, include_center=False, radius = 1) # ? Get the next possible steps
        self.currPosibleAgents = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 1) # ? Get the next possible steps
        self.nextPosition = []

        print(f'My destiny is: {self.destiny} and Im on: {self.pos}')

        if type(self.model.grid.get_cell_list_contents(self.pos)[0]) is Road or type(self.model.grid.get_cell_list_contents(self.pos)[0]) is Traffic_Light:

            # ? Check if car is on the edge
            if self.onEdge() != False:
                if self.onEdge() == "left_bottom":
                    self.nextPosition = (self.pos[0] + 1, self.pos[1])
                elif self.onEdge() == "left_top":
                    self.nextPosition = (self.pos[0], self.pos[1] - 1)
                elif self.onEdge() == "right_bottom":
                    self.nextPosition = (self.pos[0], self.pos[1] + 1)
                elif self.onEdge() == "right_top":
                    self.nextPosition = (self.pos[0] - 1, self.pos[1])

                self.prevPosition.append(self.pos)
                self.model.grid.move_agent(self, self.nextPosition)

            # ? Check if car is on the border
            elif self.onBorder() != False:
                # ? Check what border is the car on
                if self.onBorder() == "left":
                    self.nextPosition = (self.pos[0] + 1, self.pos[1])
                elif self.onBorder() == "top":
                    self.nextPosition = (self.pos[0], self.pos[1] - 1)
                elif self.onBorder() == "right":
                    self.nextPosition = (self.pos[0] - 1, self.pos[1])
                elif self.onBorder() == "bottom":
                    self.nextPosition = (self.pos[0], self.pos[1] + 1)

                self.prevPosition.append(self.pos)
                self.model.grid.move_agent(self, self.nextPosition)

            # ? Check if car is on a corner
            elif self.onCorner():
                self.nextPosition = self.currPosiblePositions
                self.numberOfPosition = []
                self.dumbmList = []
                for i in range(len(self.nextPosition)): self.numberOfPosition.append(i)

                # ! JUST BECAUSE THIS IS DUMB (NO JOKE)
                if len(self.nextPosition) != 4:

                    if len(self.nextPosition) == 3:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        if 0 not in self.dumbmList:
                            self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                        elif 1 not in self.dumbmList:
                            self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                        elif 2 not in self.dumbmList:
                            self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                        elif 3 not in self.dumbmList:
                            self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                    
                    elif len(self.nextPosition) == 2:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        for i in range(2):
                            if 0 not in self.dumbmList:
                                self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                                self.dumbmList.insert(0, 0)
                            elif 1 not in self.dumbmList:
                                self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                                self.dumbmList.insert(1, 1)
                            elif 2 not in self.dumbmList:
                                self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                                self.dumbmList.insert(2, 2)
                            elif 3 not in self.dumbmList:
                                self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                                self.dumbmList.insert(3, 3)

                    elif len(self.nextPosition) == 1:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        for i in range(3):
                            if 0 not in self.dumbmList:
                                self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                                self.dumbmList.insert(0, 0)
                            elif 1 not in self.dumbmList:
                                self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                                self.dumbmList.insert(1, 1)
                            elif 2 not in self.dumbmList:
                                self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                                self.dumbmList.insert(2, 2)
                            elif 3 not in self.dumbmList:
                                self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                                self.dumbmList.insert(3, 3)

                # ? Check if the car is near an edge
                if self.nearEdge() != None:
                    if self.nearEdge() == "left_bottom":
                        self.nextPosition = (self.pos[0] + 1, self.pos[1])
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)
                    elif self.nearEdge() == "left_top":
                        self.nextPosition = (self.pos[0], self.pos[1] - 1)
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)
                    elif self.nearEdge() == "right_bottom":
                        self.nextPosition = (self.pos[0], self.pos[1] + 1)
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)
                    elif self.nearEdge() == "right_top":
                        self.nextPosition = (self.pos[0] - 1, self.pos[1])
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)

                # ? Check if the car is near a border
                elif self.nearBorder() != None:
                    if self.nearBorder() == "left": 
                        self.nextPosition.remove(self.nextPosition[0])
                        self.nextPosition.remove(self.nextPosition[1])
                        # * CURR POSITIONS [south, east]
                        if type(self.model.grid.get_cell_list_contents(self.nextPosition[1])[0]) is Traffic_Light and self.whatDirImOn() == "south":
                            self.nextPosition = self.nextPosition[0]
                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)
                        elif type(self.model.grid.get_cell_list_contents(self.nextPosition[1])[0]) is Road:
                            if self.model.grid.get_cell_list_contents(self.nextPosition[1])[0].direction == "west":
                                self.nextPosition = self.nextPosition[0]
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)
                            else:
                                self.nextPosition = self.random.choice(self.nextPosition)
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)

                    elif self.nearBorder() == "top":
                        self.nextPosition.remove(self.nextPosition[2])
                        self.nextPosition.remove(self.nextPosition[2])
                        # * CURR POSITIONS [west, south]
                        if type(self.model.grid.get_cell_list_contents(self.nextPosition[1])[0]) is Traffic_Light and self.whatDirImOn() == "west":
                            self.nextPosition = self.nextPosition[0]
                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)
                        elif type(self.model.grid.get_cell_list_contents(self.nextPosition[1])[0]) is Road:
                            if self.model.grid.get_cell_list_contents(self.nextPosition[1])[0].direction == "north":
                                self.nextPosition = self.nextPosition[0]
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)
                            else:
                                self.nextPosition = self.random.choice(self.nextPosition)
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)

                    elif self.nearBorder() == "right":
                        self.nextPosition.remove(self.nextPosition[3])
                        self.nextPosition.remove(self.nextPosition[1])
                        # * CURR POSITIONS [west, north]
                        if type(self.model.grid.get_cell_list_contents(self.nextPosition[0])[0]) is Traffic_Light and self.whatDirImOn() == "north":
                            self.nextPosition = self.nextPosition[1]
                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)
                        elif type(self.model.grid.get_cell_list_contents(self.nextPosition[0])[0]) is Road:
                            if self.model.grid.get_cell_list_contents(self.nextPosition[0])[0].direction == "east":
                                self.nextPosition = self.nextPosition[1]
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)
                            else:
                                self.nextPosition = self.random.choice(self.nextPosition)
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)

                    elif self.nearBorder() == "bottom":
                        self.nextPosition.remove(self.nextPosition[1])
                        self.nextPosition.remove(self.nextPosition[0])
                        # * CURR POSITIONS [north, east]
                        if type(self.model.grid.get_cell_list_contents(self.nextPosition[0])[0]) is Traffic_Light and self.whatDirImOn() == "east":
                            self.nextPosition = self.nextPosition[1]
                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)
                        elif type(self.model.grid.get_cell_list_contents(self.nextPosition[0])[0]) is Road:
                            if self.model.grid.get_cell_list_contents(self.nextPosition[0])[0].direction == "south":
                                self.nextPosition = self.nextPosition[1]
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)
                            else:
                                self.nextPosition = self.random.choice(self.nextPosition)
                                self.prevPosition.append(self.pos)
                                self.model.grid.move_agent(self, self.nextPosition)

                # ? The car is on the city
                else:
                    if self.whatDirImOn() == "north":
                        self.nextPosition.remove(self.nextPosition[1])
                        # * CURR POSITIONS [west, north, east]

                        if self.whatDirItIs(self.nextPosition[0]) == "south":
                            self.nextPosition.remove(self.nextPosition[0])
                            # * CURR POSITIONS [north, east]
                            if self.whatDirItIs(self.nextPosition[1]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[1])

                        elif self.whatDirItIs(self.nextPosition[2]) == "south":
                            self.nextPosition.remove(self.nextPosition[2])
                            # * CURR POSITIONS [west, north]
                            if self.whatDirItIs(self.nextPosition[0]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[0])

                        if len(self.nextPosition) == 1:
                            self.nextPosition = self.nextPosition[0]
                        else:
                            self.nextPosition = self.random.choice(self.nextPosition)

                    elif self.whatDirImOn() == "south":
                        self.nextPosition.remove(self.nextPosition[2])
                        # * CURR POSITIONS [west, south, east]

                        if self.whatDirItIs(self.nextPosition[0]) == "north":
                            self.nextPosition.remove(self.nextPosition[0])
                            # * CURR POSITIONS [south, east]
                            if self.whatDirItIs(self.nextPosition[1]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[1])

                        elif self.whatDirItIs(self.nextPosition[1]) == "north":
                            self.nextPosition.remove(self.nextPosition[1])
                            # * CURR POSITIONS [west, south]
                            if self.whatDirItIs(self.nextPosition[0]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[0])

                        if len(self.nextPosition) == 1:
                            self.nextPosition = self.nextPosition[0]
                        else:
                            self.nextPosition = self.random.choice(self.nextPosition)

                    elif self.whatDirImOn() == "east":
                        self.nextPosition.remove(self.nextPosition[0])
                        # * CURR POSITIONS [south, north, east]
                        if self.whatDirItIs(self.nextPosition[0]) == "west":
                            self.nextPosition.remove(self.nextPosition[0])
                            # * CURR POSITIONS [north, east]
                            if self.whatDirItIs(self.nextPosition[0]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[0])

                        elif self.whatDirItIs(self.nextPosition[1]) == "west":
                            self.nextPosition.remove(self.nextPosition[1])
                            # * CURR POSITIONS [south, east]
                            if self.whatDirItIs(self.nextPosition[0]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[0])

                        if len(self.nextPosition) == 1:
                            self.nextPosition = self.nextPosition[0]
                        else:
                            self.nextPosition = self.random.choice(self.nextPosition)

                    elif self.whatDirImOn() == "west":
                        self.nextPosition.remove(self.nextPosition[3])
                        # * CURR POSITIONS [west, south, north]
                        if self.whatDirItIs(self.nextPosition[1]) == "east":
                            self.nextPosition.remove(self.nextPosition[1])
                            # * CURR POSITIONS [west, north]
                            if self.whatDirItIs(self.nextPosition[1]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[1])

                        elif self.whatDirItIs(self.nextPosition[2]) == "east":
                            self.nextPosition.remove(self.nextPosition[2])
                            # * CURR POSITIONS [west, south]
                            if self.whatDirItIs(self.nextPosition[1]) == self.whatDirImOn():
                                self.nextPosition.remove(self.nextPosition[1])

                        if len(self.nextPosition) == 1:
                            self.nextPosition = self.nextPosition[0]
                        else:
                            self.nextPosition = self.random.choice(self.nextPosition)

                    self.prevPosition.append(self.pos)
                    self.model.grid.move_agent(self, self.nextPosition)

            # ? The car is on road (No border or edge or corner)
            else: 
                # ? Move on road
                self.nextPosition = self.model.grid.get_neighborhood(self.pos,moore=False, include_center=False, radius = 1)
                self.numberOfPosition = []
                self.dumbmList = []

                # ! JUST BECAUSE THIS IS DUMB (NO JOKE)
                if len(self.nextPosition) != 4:

                    if len(self.nextPosition) == 3:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        if 0 not in self.dumbmList:
                            self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                        elif 1 not in self.dumbmList:
                            self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                        elif 2 not in self.dumbmList:
                            self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                        elif 3 not in self.dumbmList:
                            self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                    
                    elif len(self.nextPosition) == 2:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        for i in range(2):
                            if 0 not in self.dumbmList:
                                self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                                self.dumbmList.insert(0, 0)
                            elif 1 not in self.dumbmList:
                                self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                                self.dumbmList.insert(1, 1)
                            elif 2 not in self.dumbmList:
                                self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                                self.dumbmList.insert(2, 2)
                            elif 3 not in self.dumbmList:
                                self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                                self.dumbmList.insert(3, 3)

                    elif len(self.nextPosition) == 1:
                        for pos in self.nextPosition:
                            if self.whatDirItIs(pos) == "west":
                                self.dumbmList.append(0)
                            elif self.whatDirItIs(pos) == "south":
                                self.dumbmList.append(1)
                            elif self.whatDirItIs(pos) == "north":
                                self.dumbmList.append(2)
                            elif self.whatDirItIs(pos) == "east":
                                self.dumbmList.append(3)

                        for i in range(3):
                            if 0 not in self.dumbmList:
                                self.nextPosition.insert(0, (self.pos[0] - 1, self.pos[1]))
                                self.dumbmList.insert(0, 0)
                            elif 1 not in self.dumbmList:
                                self.nextPosition.insert(1, (self.pos[0], self.pos[1] -1))
                                self.dumbmList.insert(1, 1)
                            elif 2 not in self.dumbmList:
                                self.nextPosition.insert(2, (self.pos[0], self.pos[1] + 1))
                                self.dumbmList.insert(2, 2)
                            elif 3 not in self.dumbmList:
                                self.nextPosition.insert(3, (self.pos[0] + 1, self.pos[1]))
                                self.dumbmList.insert(3, 3)

                if len(self.nextPosition) > 2:

                    # ? Check if the car is near its destiny
                    if self.destiny in self.nextPosition:
                        self.nextPosition = self.destiny
                        self.arrived = True
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)

                    # ? If car is right on a traffic light
                    elif self.whatDirImOn() == "traffic_light":
                        if self.whatDirItIs(self.prevPosition[-1]) == "west":
                            self.nextPosition = self.nextPosition[0]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "north":
                            self.nextPosition = self.nextPosition[2]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "east":
                            self.nextPosition = self.nextPosition[3]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "south":
                            self.nextPosition = self.nextPosition[1]

                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)

                    # ? Car is just in road
                    else:

                        if self.whatDirImOn() == "west":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[0]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[0]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[0]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[0]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[0]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[0]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "north":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[2]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[2]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[2]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[2]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[2]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[2]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "east":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[3]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[3]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[3]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[3]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[3]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[3]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "south":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[1]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[1]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[1]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[1]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[1]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[1]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                else:
                    # ? Check if the car is near its destiny
                    if self.destiny in self.nextPosition:
                        self.nextPosition = self.destiny
                        self.arrived = True
                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)

                    # ? If car just passed a traffic light not care for others
                    elif self.whatDirItIs(self.prevPosition[-1]) == "traffic_light" or self.whatDirItIs(self.prevPosition[-2]) == "traffic_light":
                        if self.whatDirImOn() == "west":
                            # ? Check if on the next step there is a car
                            if len(self.model.grid.get_cell_list_contents([self.nextPosition[0]])) > 1:
                                self.nextPosition = self.pos
                            else:
                                self.nextPosition = self.nextPosition[0]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "north":
                            # ? Check if on the next step there is a car
                            if len(self.model.grid.get_cell_list_contents([self.nextPosition[2]])) > 1:
                                self.nextPosition = self.pos
                            else:
                                self.nextPosition = self.nextPosition[2]
                            
                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "east":
                            # ? Check if on the next step there is a car
                            if len(self.model.grid.get_cell_list_contents([self.nextPosition[3]])) > 1:
                                self.nextPosition = self.pos
                            else:
                                self.nextPosition = self.nextPosition[3]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "south":
                            # ? Check if on the next step there is a car
                            if len(self.model.grid.get_cell_list_contents([self.nextPosition[1]])) > 1:
                                self.nextPosition = self.pos
                            else:
                                self.nextPosition = self.nextPosition[1]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                    # ? If car is right on a traffic light
                    elif self.whatDirImOn() == "traffic_light":
                        if self.whatDirItIs(self.prevPosition[-1]) == "west":
                            self.nextPosition = self.nextPosition[0]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "north":
                            self.nextPosition = self.nextPosition[2]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "east":
                            self.nextPosition = self.nextPosition[3]
                        elif self.whatDirItIs(self.prevPosition[-1]) == "south":
                            self.nextPosition = self.nextPosition[1]

                        self.prevPosition.append(self.pos)
                        self.model.grid.move_agent(self, self.nextPosition)

                    # ? Car is just in road
                    else:

                        if self.whatDirImOn() == "west":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[0]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[0]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[0]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[0]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[0]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[0]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "north":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[2]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[2]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[2]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[2]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[2]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[2]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "east":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[3]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[3]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[3]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[3]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[3]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[3]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)

                        elif self.whatDirImOn() == "south":
                            # ? Check for traffic lights on front of the car
                            if self.whatDirItIs(self.nextPosition[1]) == "traffic_light":
                                if self.model.grid.get_cell_list_contents([self.nextPosition[1]])[0].state == False:
                                    self.nextPosition = self.pos
                                else:
                                    # ? Check if on the next step there is a car
                                    if len(self.model.grid.get_cell_list_contents([self.nextPosition[1]])) > 1:
                                        self.nextPosition = self.pos
                                    else:
                                        self.nextPosition = self.nextPosition[1]
                            else:
                                # ? Check if on the next step there is a car
                                if len(self.model.grid.get_cell_list_contents([self.nextPosition[1]])) > 1:
                                    self.nextPosition = self.pos
                                else:
                                    self.nextPosition = self.nextPosition[1]

                            self.prevPosition.append(self.pos)
                            self.model.grid.move_agent(self, self.nextPosition)


            if self.whatDirImOn() == "traffic_light":
                self.facing = self.whatDirItIs(self.prevPosition[-1])
            else:
                self.facing = self.whatDirImOn()

        else:
            self.status = False

    def onEdge(self):
        ''' Check if car is on the edge of the grid 

            Args:
                - self: Instance of the class

            Returns:
                - "left_bottom": If car is on the left bottom edge
                - "right_bottom": If car is on the right bottom edge
                - "left_top": If car is on the left top edge
                - "right_top": If car is on the right top edge
                - False: If car is not on the edge of the grid
        '''
        if (self.pos[0] == 0) and (self.pos[1] == 0):
            return "left_bottom"
        elif (self.pos[0] == 0) and (self.pos[1] == self.model.grid.height - 1):
            return "left_top"
        elif (self.pos[0] == self.model.grid.width - 1) and (self.pos[1] == 0):
            return "right_bottom"
        elif (self.pos[0] == self.model.grid.width - 1 ) and (self.pos[1] == self.model.grid.height - 1):
            return "right_top"
        else:
            return False

    def onBorder(self):
        ''' Check if car is on the border of the grid

            Args:
                - self: Instance of the class

            Returns:
                - "left": If car is on the left border of the grid
                - "right": If car is on the right border of the grid
                - "bottom": If car is on the bottom border of the grid
                - "top": If car is on the top border of the grid
                - False: If car is not on the border of the grid
        '''
        if (self.pos[0] == 0):
            return "left"
        elif (self.pos[0] == self.model.grid.width - 1):
            return "right"
        elif (self.pos[1] == 0):
            return "bottom"
        elif (self.pos[1] == self.model.grid.height - 1):
            return "top"
        else:
            return False

    def whatDirImOn(self):
        ''' Check what is on the position where the car is
            
                Args:
                    - self: Instance of the class
    
                Returns:
                    - Road.direction: If current position is a road
                    - "traffic_light": If current position is a traffic light
            '''
        for agent in  self.model.grid.get_cell_list_contents(self.pos):
            if type(agent) is Road:
                return agent.direction
            elif type(agent) is Traffic_Light:
                return "traffic_light"

    def whatDirItIs(self,direction):
        ''' Check what is on the direction of a position
                
                    Args:
                        - self: Instance of the class
                        - direction: Position (x,y) of the grid
        
                    Returns:
                        - Road.direction: If next position is a road [east, west, north, south]
                        - "traffic_light": If next position is a traffic light
                '''
        for agent in self.model.grid.get_cell_list_contents(direction):
            if type(agent) is Road:
                return agent.direction
            elif type(agent) is Traffic_Light:
                return "traffic_light"

    def onCorner(self):
        ''' Check if car is on the corner of the grid
            
                Args:
                    - self: Instance of the class
    
                Returns:
                    - True: If car is on the corner of a street
                    - False: If car is not on the corner of a street
            '''
        temp = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 1)
        for agent in temp:
            if type(agent) is not Road:
                temp.remove(agent)
        if len(temp) == 4:
            return True
        else:
            return False

    def nearEdge(self):
        ''' Check if car is near the edge of the grid
            
                Args:
                    - self: Instance of the class
    
                Returns:
                    - "left_bottom": If car is near the left bottom edge
                    - "right_bottom": If car is near the right bottom edge
                    - "left_top": If car is near the left top edge
                    - "right_top": If car is near the right top edge
                    - None: If car is not near the edge of the grid
            '''
        if self.pos == (1,1):
            return "left_bottom"
        elif self.pos == (1,self.model.grid.height - 2):
            return "left_top"
        elif self.pos == (self.model.grid.width - 2,1):
            return "right_bottom"
        elif self.pos == (self.model.grid.width - 2,self.model.grid.height - 2):
            return "right_top"

    def nearBorder(self):
        ''' Check if car is near the border of the grid
            
                Args:
                    - self: Instance of the class
    
                Returns:
                    - "left": If car is near the left border of the grid
                    - "right": If car is near the right border of the grid
                    - "bottom": If car is near the bottom border of the grid
                    - "top": If car is near the top border of the grid
                    - None: If car is not near the border of the grid
        ''' 
        if self.pos[0] == 1:
            return "left"
        elif self.pos[0] == self.model.grid.width - 2:
            return "right"
        elif self.pos[1] == 1:
            return "bottom"
        elif self.pos[1] == self.model.grid.height - 2:
            return "top"

class Traffic_Light(Agent):
    ''' Class that represents traffic lights agent 

        Methods:
            - __init__: Constructor of the class
            - step: Method that represents the traffic light behaviour
            - changeState: Method that changes the state of the traffic light
            - nearTL: Method that checks if there is a traffic light near the current one
            - myPair: Method that returns the pair of the current traffic light
            - hasCar: Method that checks if there is a car in front of the traffic light
    '''
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        ''' Constructor of the traffic light class

            Parameters:
                - unique_id: Unique id of the agent
                - model: Instance of the model
                - state: State of the traffic light
                - timeToChange: Time to change the state of the traffic light
            
            Attributes:
                - unique_id: Unique id of the agent
                - model: Instance of the model
                - state: State of the traffic light
                - timeToChange: Time to change the state of the traffic light

        '''
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange
        self.neighTL = []

    def step(self):
        ''' Method that represents the traffic light behaviour
            
                Args:
                    - self: Instance of the class
                
                Returns:
                    - None
            '''
        self.changeState()

    def changeState(self):
        ''' Method that changes the state of the traffic light
                
                    Args:
                        - self: Instance of the class
                    
                    Returns:
                        - None
                '''
        self.neighTL = self.model.grid.get_neighborhood(self.pos,moore=True, include_center=False, radius = 1)
        self.pair = self.myPair()

        if self.state == True:
            self.pair.state = True
        else:
            self.pair.state = False

        if self.nearTL() != None:
            if self.hasCar():
                self.state = True
                self.pair.state = True
                self.model.grid.get_cell_list_contents(self.nearTL())[0].state = False
            else:
                self.state = False
                self.pair.state = False
                self.model.grid.get_cell_list_contents(self.nearTL())[0].state = True

    def nearTL(self):
        ''' Method that checks if there is a traffic light near the current one

            Args:
                - self: Instance of the class

            Returns:
                - None: If there is no traffic light near the current one
                - (x,y): Position of the traffic light near the current one
        '''
        tlPos = None
        if self.pos[1] == 0:
            tlPos = (self.pos[0] + 1,self.pos[1] + 2)
        elif self.pos[1] == self.model.grid.height - 1:
            tlPos = (self.pos[0] - 1,self.pos[1] - 2)
        elif self.pos[0] == 0:
            tlPos = (self.pos[0] + 2,self.pos[1] - 1)
        elif self.pos[0] == self.model.grid.width - 1:
            tlPos = (self.pos[0] - 2,self.pos[1] + 1)
        elif self.pos[0] == 7 and self.pos[1] == self.model.grid.height - 7:
            tlPos = (self.pos[0] + 1,self.pos[1] + 1)
        return tlPos

    def myPair(self):
        ''' Method that returns the pair of the current traffic light

            Args:
                - self: Instance of the class

            Returns:
                - pair: Pair of the current traffic light
        '''
        for agent in self.model.grid.get_neighbors(self.pos, moore=False, include_center=False, radius = 1):
            if type(agent) is Traffic_Light:
                return agent

    def hasCar(self):
        ''' Method that checks if there is a car in front of the traffic light
            
                Args:
                    - self: Instance of the class
    
                Returns:
                    - True: If there is a car in front of the traffic light
                    - None: If there is no car in front of the traffic light
            '''
        for agent in self.model.grid.get_neighbors(self.pos, moore=False, include_center=False, radius = 1):
            if type(agent) is Car:
                return True

class Road(Agent):
    ''' Class that represents road agent
    
            Methods:
                - __init__: Constructor of the class
                - step: Method that represents the road behaviour
        '''
    def __init__(self, unique_id, model, direction):
        ''' Constructor of the road class
            
            Parameters:
                - unique_id: Unique id of the agent
                - model: Instance of the model
                - direction: Direction of the road

            Attributes:
                - unique_id: Unique id of the agent
                - model: Instance of the model
                - direction: Direction of the road
        '''
        super().__init__(unique_id, model)
        self.direction = direction # ?  Direction of the road [north, south, east, west]

        ''' Method that represents a step
            
            Args:
                - self: Instance of the class

            Returns:
                - None
        '''
        pass

class Destination(Agent):
    ''' Class that represents destination agent
    
        Methods:
            - __init__: Constructor of the class

    '''
    def __init__(self, unique_id, model):
        ''' Constructor of the destination class
            
            Parameters:
                - unique_id: Unique id of the agent
                - model: Instance of the model

            Attributes:
                - unique_id: Unique id of the agent
                - model: Instance of the model
        '''
        super().__init__(unique_id, model)

class Obstacle(Agent):
    ''' Class that represents obstacle agent
    
        Methods:
            - __init__: Constructor of the class
            
    '''

    def __init__(self, unique_id, model):
        ''' Constructor of the obstacle class
            
            Parameters:
                - unique_id: Unique id of the agent
                - model: Instance of the model

            Attributes:
                - unique_id: Unique id of the agent
                - model: Instance of the model
        '''
        super().__init__(unique_id, model)

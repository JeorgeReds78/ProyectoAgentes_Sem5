"""
    Bot class and Box class for the model.

    Authors:
        - Carlos Alan Gallegos Espindola  (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Omar Rodrigo Talavera Becerra	  (A01752221)
        - Jorge Rojas Rivas			      (A01745334)

    Date of creation: 16/11/2022
    Last Modification: 21/11/2022
"""

import mesa # Base class for agents

class Bot(mesa.Agent):
    ''' Class that represents the bots in the model 

        Methods:
            - __init__: Constructor of the class
            - step: Method that is called every step of the model
            - move: Method that makes the bot move
            - seeBox: Method that checks if the bot can see a box
            - seenBoxes: Method that adds the boxes that the bot can see to the vision list
            - pickBox: Method that makes the bot pick a box
            - dropBox: Method that makes the bot drop a box at destination
    '''
    def __init__(self, unique_id, model, hasBox, maxBoxes):
        ''' Constructor of the Bot class
        
            Parameters:
                - unique_id: Unique id of the bot
                - model: Model where the bot is
                - hasBox: Boolean that indicates if the bot has a box
                - maxBoxes: Maximum number of boxes that the bot can carry
                
                Attributes:
                    - vision: List of the boxes that the bot can see
                    - boxVision: List of the boxes that the bot can see
                    - possibleSee: List of the possible cells that the bot can see
                    - possibleSteps: List of the possible cells that the bot can move to
                    - boxID: Unique id of the box that the bot is carrying
                    - hasBox: Boolean that indicates if the bot has a box
                    - maxBoxes: Maximum number of boxes that the bot can carry
                    
        '''
        super().__init__(unique_id, model)
        self.hasBox = hasBox
        self.boxID = 0
        self.maxBoxes = maxBoxes
        self.finished = False

    def step(self):
        ''' Method that is called every step of the model 
            
            Args:
                - self: Instance of the class
                
            Returns:
                - None
        '''
        self.move()

    def move(self):
        ''' Method that makes the bot move 
        
            Args:
                - self: Instance of the class
                
            Returns:
                - None
        '''
        destination = [(0,0),(0,3),(0,6),(0,9)]
        # ? Vision of box && Vision list
        self.vision = []
        self.boxVision = [p for p in self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)]
        # ? Possible see list
        self.possibleSee = [p for p in self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)]
        see = self.model.grid.get_neighbors(self.pos, moore = False, include_center = False)
        # ? Steps list with the possible steps to take (without other agents)
        self.possibleSteps = [p for p in self.model.grid.get_neighborhood(self.pos, moore = False, include_center = True)]
        agentsCell = self.model.grid.get_neighbors(self.pos, moore = False, include_center = True, radius = 1)

        # ? Cant move to destination cells
        for position in destination:
            if position in self.possibleSteps:
                self.possibleSteps.remove(position)

        # ? Cant move to cells with other agents 
        for agent in agentsCell:
            if type(agent) == Bot:
                if agent.pos in self.possibleSteps:
                    self.possibleSteps.remove(agent.pos)

        # ? Cant move to box position
        for box in see:
            if type(box) == Box:
                if box.pos in self.possibleSteps:
                    self.possibleSteps.remove(box.pos)

        # ? Only see box if it is in the vision
        if self.seeBox() == False:
            self.vision = []
        else:
            self.seenBoxes()

        # ? Choose next move
        if len(self.possibleSteps) == 0:
                newPosition = self.pos
        elif len(self.possibleSteps) == 1:
            newPosition = self.possibleSteps[0]
        else:
            newPosition = self.random.choice(self.possibleSteps)

        self.check()
        if self.hasBox == True:
            # ? If the bot has a box, it will drop it in the destination
            for position in self.possibleSee:
                if position in destination:
                    self.dropBox()
                else:
                    self.model.grid.move_agent(self, newPosition)
        else:
            # ? If the bot doesn't have a box, it will pick one if it is in the vision
            if self.seeBox():
                self.seenBoxes()
                if len(self.vision) > 1:
                    self.vision = self.random.choice(self.vision)
                    self.pickBox()
                elif len(self.vision) == 1:
                    self.pickBox()
            else:
                self.model.grid.move_agent(self, newPosition)

    def seeBox(self):
        ''' Method that checks if the bot can see a box
        
            Args:
                - self: Instance of the class
            
            Returns:
                - Boolean: True if the bot can see a box, False if it can't
        '''
        for agent in self.boxVision:    
            if type(agent) == Box and agent.pickable == True:
                return True
        return False

    def seenBoxes(self):
        ''' Method that adds the boxes that the bot can see to the vision list
            
            Args:
                - self: Instance of the class
                
            Returns:
                - None
        '''
        for agent in self.boxVision:
            self.vision.append(agent.pos)

    def pickBox(self):
        ''' Method that makes the bot pick a box
        
            Args:
                - self: Instance of the class
            
            Returns:
                - None
        '''
        for agent in self.boxVision:
            if type(agent) == Box and agent.pickable == True and agent.pos == self.vision:
                self.boxID = agent.unique_id
                agent.picked = True
                self.hasBox = True

    def dropBox(self):
        ''' Method that makes the bot drop a box at destination
        
            Args:
                - self: Instance of the class
            
            Returns:
                - None
        '''
        for destination in self.possibleSee:
            if destination == (0,0) or destination == (0,3) or destination == (0,6) or destination == (0,9):
                if len(self.boxVision) > 5:
                    self.model.grid.move_agent(self, self.possibleSteps[0])
                else:
                    agentToP = Box(self.boxID, self.model, False, False, False)
                    self.model.grid.place_agent(agentToP, destination)

                    for agent in self.boxVision:
                        if type(agent) == Box and agent.unique_id == self.boxID:
                            agent.arrived = True
                    
                    self.boxID = 0
                    self.hasBox = False

    def check(self):
        ''' Method that checks if the bot has finished
        
            Args:
                - self: Instance of the class
                
            Returns:
                - None
        '''
        destination = [(0,0),(0,3),(0,6),(0,9)]
        sum = 0
        self.finished = False
        for position in destination:
            if len(self.model.grid.get_neighbors(position, moore=False, include_center=True, radius=0)) != 0:
                sum += len(self.model.grid.get_neighbors(position, moore=False, include_center=True, radius=0)) 
        if sum == self.maxBoxes:
            self.finished = True

class Box(mesa.Agent):
    ''' Class that represents a box 

        Methods:
            - __init__: Constructor of the class
            - step: Method that makes the box move
    '''

    def __init__(self, unique_id, model, picked: bool, arrived: bool, pickable: bool):
        ''' Constructor of the class
        
            Args:
                - self: Instance of the class
                - unique_id: Unique id of the box
                - model: Instance of the model
                - picked: Boolean that indicates if the box has been picked
                - arrived: Boolean that indicates if the box has arrived to destination
                - pickable: Boolean that indicates if the box can be picked
            
            Returns:
                - None
        '''
        super().__init__(unique_id, model)
        self.picked = picked
        self.arrived = arrived
        self.pickable = pickable

    def step(self):
        ''' Method that makes the box move
        
            Args:
                - self: Instance of the class
            
            Returns:
                - None
        '''
        self.move()

    def move(self):
        ''' Method that makes the box move

            Args:
                - self: Instance of the class

            Returns:
                - None
        '''
        destination = [(0,0),(0,3),(0,6),(0,9)]
        if self.arrived == False:
            if self.pos in destination:
                self.arrived = True
            else:
                if self.pickable == True:
                    if self.picked == True:
                        self.model.grid.remove_agent(self)
                        self.pickable = False
        else:
            return None
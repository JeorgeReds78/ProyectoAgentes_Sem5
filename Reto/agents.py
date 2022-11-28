from mesa import Agent
import queue

'''
    Remember that this is the look
NorthWest         North         NorthEast  
        x-1,y+1 | x-1,y | x-1,y+1
West    x,y-1   | x,y   | x,y+1    East
        x+1,y-1 | x+1,y | x+1,y+1
SouthWest         South         SouthEast
'''

'''
    Borders representations:  (M = Max)
    0,0 LeftBottom
    0,M TopLeft
    M,0 BottomRight
    M,M TopRight
'''

class Car(Agent):
    def __init__(self, unique_id, model, destiny):
        super().__init__(unique_id, model)
        self.facing = None # ?  Direction the car is facing [0, 90, 180, 270] For Unity
        self.destiny = destiny # ?  Destination of the car to arrive
        self.nextPosition = None # ?  Next position of the car 
        # TODO: Implement GPS function (ADVANCED VERSION)
        #self.roadToFollow = None # ? Road to follow {lst}
        # TODO: Implement GPS function (ADVANCED VERSION)
        self.arrived = False
        self.prevPosition = []
        self.prevPositionTL = []


    def step(self):
        if not self.arrived:
            self.move()

    def move(self):
        # ? Check for traffic lights
        # ? Check for obstacles
        # ? Check for roads
        # ? Move
        # self.actualPos = self.pos
        self.currPosiblePositions = self.model.grid.get_neighborhood(self.pos,moore=False, include_center=False, radius = 1) # ? Get the next possible steps
        self.currPosibleAgents = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 1) # ? Get the next possible steps
        roadsHood, obstaclesHood, trafficLightsHood = self.getVisionPositions()
        roadsBors, obstaclesBors, trafficLightsBors = self.getVisionAgents()
        self.nextPosition = []

        # ? Check if car is on the edge
        if self.onEdge():
            print("On edge")
            self.moveOnEdge()

        # ? Check if car is on the border
        elif self.onBorder():
            print("On border")
            # ? Check what border is the car on
            currborder = self.whatBorder()
            if currborder == "left":
                self.nextPosition = (self.pos[0] + 1, self.pos[1])
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif currborder == "top":
                self.nextPosition = (self.pos[0], self.pos[1] - 1)
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif currborder == "right":
                self.nextPosition = (self.pos[0] - 1, self.pos[1])
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif currborder == "bottom":
                self.nextPosition = (self.pos[0], self.pos[1] + 1)
                
                self.model.grid.move_agent(self, self.nextPosition)

        # ? Now we are out of the border
        else:
            # ? Check if we are on a corner
            if self.onCorner():
                print("On corner")
                # ? Clean the next possible positions
                self.nextPosition = self.currPosiblePositions
                # ? Prevent the car from going on reverse
                if type(self.nextPosition) == list:
                    for direction in self.nextPosition:
                        if self.whatDirImOn() == "west" and self.pos[0] < direction[0]:
                            self.nextPosition.remove(direction)
                        elif self.whatDirImOn() == "east" and self.pos[0] > direction[0]:
                            self.nextPosition.remove(direction)
                        elif self.whatDirImOn() == "south" and self.pos[1] < direction[1]:
                            self.nextPosition.remove(direction)
                        elif self.whatDirImOn() == "north" and self.pos[1] > direction[1]:
                            self.nextPosition.remove(direction)
                
            else:
                print(f'Not on corner')
                self.nextPosition = self.currPosiblePositions
                # ? Prevent from swaping road to right or left
                for direction in self.nextPosition:
                    if (self.whatDirImOn() == "west" and self.pos[1] != direction[1]) or (self.whatDirImOn() == "east" and self.pos[1] != direction[1]):
                        self.nextPosition.remove(direction)
                    elif (self.whatDirImOn() == "south" and self.pos[0] != direction[0]) or (self.whatDirImOn() == "north" and self.pos[0] != direction[0]):
                        self.nextPosition.remove(direction)

        print(f'Next position 1 : {self.nextPosition}  Actual position : {self.pos}')
        # ? Clean postion list from going on reverse
        if type(self.nextPosition) == list:
            for direction in self.nextPosition:
                if self.whatDirImOn() == "west" and self.pos[0] < direction[0]:
                    self.nextPosition.remove(direction)
                elif self.whatDirImOn() == "east" and self.pos[0] > direction[0]:
                    self.nextPosition.remove(direction)
                elif self.whatDirImOn() == "south" and self.pos[1] < direction[1]:
                    self.nextPosition.remove(direction)
                elif self.whatDirImOn() == "north" and self.pos[1] > direction[1]:
                    self.nextPosition.remove(direction)
                elif self.whatDirImOn() == "traffic_light":
                    self.nextPosition.remove(direction)

        print(f'Next position 2 : {self.nextPosition}  Actual position : {self.pos}')

        if type(self.nextPosition) == list:
            for direction in self.nextPosition:
                if self.prevPosition[-1] == direction:
                    self.nextPosition.remove(direction)

        # ? Check if the next position is a road
        if type(self.nextPosition) == list:
            for direction in self.nextPosition:
                for agent in self.model.grid.get_cell_list_contents(direction):
                    if type(agent) is not Road and type(agent) is not Traffic_Light:
                        self.nextPosition.remove(direction)

        print(f'Next position 3 : {self.nextPosition}  Actual position : {self.pos}')
        # ? Dont go to border 
        if type(self.nextPosition) == list:
            for direction in self.nextPosition:
                if len(self.model.grid.get_neighborhood(direction, moore=False, include_center=False, radius=1) ) == 3:
                    self.nextPosition.remove(direction)

        print(f'Next position 4 : {self.nextPosition}  Actual position : {self.pos}')
        # ? Not care for 2 traffic lights at the time
        if type(self.nextPosition) == list:
            for direction in self.nextPosition:
                for agent in self.model.grid.get_cell_list_contents(direction):
                    if (self.whatDirImOn() == "west" or self.whatDirImOn() == "east") and (type(agent) is Traffic_Light):
                        if self.pos[1] != direction[1]:
                            print(f'Position remover 1 : {direction}')
                            self.nextPosition.remove(direction)
                    elif(self.whatDirImOn() == "north" or self.whatDirImOn() == "south") and (type(agent) is Traffic_Light):
                        if self.pos[0] != direction[0]:
                            print(f'Position remover 2 : {direction}')
                            self.nextPosition.remove(direction)


            print(f'Next position 5 : {self.nextPosition}  Actual position : {self.pos}')
            if type(self.nextPosition) == list and len (self.nextPosition) > 0:
                self.nextPosition = self.random.choice(self.nextPosition)
            for agent in self.model.grid.get_cell_list_contents(self.nextPosition):
                if type(agent) is Traffic_Light:
                    if (self.whatDirImOn() == "west" or self.whatDirImOn() == "east") and (agent.pos[1] == self.pos[1]):
                        if agent.state == False: # ? If the traffic light is red (False = Red)
                            
                            self.model.grid.move_agent(self, self.pos)
                        else:
                            
                            self.model.grid.move_agent(self, self.nextPosition)
                    elif (self.whatDirImOn() == "north" or self.whatDirImOn() == "south") and (agent.pos[0] == self.pos[0]):
                        if agent.state == False: # ? If the traffic light is red (False = Red)
                            
                            self.model.grid.move_agent(self, self.pos)
                        else:
                            
                            self.model.grid.move_agent(self, self.nextPosition)
                    
                elif type(agent) is not Obstacle and type(agent) is not Car:
                    
                    self.model.grid.move_agent(self, self.nextPosition)
        self.prevPosition.append(self.pos)

    def getVisionPositions(self):
        hoodVision = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 2)
        roadsHood = []
        obstaclesHood = []
        trafficLightsHood = []

        for agent in hoodVision:
            if agent == type(Road):
                roadsHood.append(agent)
            elif agent == type(Obstacle):
                obstaclesHood.append(agent)
            elif agent == type(Traffic_Light):
                trafficLightsHood.append(agent)
        
        return roadsHood, obstaclesHood, trafficLightsHood

    def getVisionAgents(self):
        borsVision = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 2)
        roadsBors = []
        obstaclesBors = []
        trafficLightsBors = []

        for agent in borsVision:
            if agent == type(Road):
                roadsBors.append(agent)
            elif agent == type(Obstacle):
                obstaclesBors.append(agent)
            elif agent == type(Traffic_Light):
                trafficLightsBors.append(agent)
        
        return roadsBors, obstaclesBors, trafficLightsBors

    def moveOnEdge(self):
        # ? Check if car is on the edge
        if self.onEdge():
            # ? Check what edge is the car on
            curredge = self.whatEdge()
            if curredge == "left_bottom":
                self.nextPosition = (self.pos[0] + 1, self.pos[1])
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif curredge == "left_top":
                self.nextPosition = (self.pos[0], self.pos[1] - 1)
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif curredge == "right_bottom":
                self.nextPosition = (self.pos[0], self.pos[1] + 1)
                
                self.model.grid.move_agent(self, self.nextPosition)
            elif curredge == "right_top":
                self.nextPosition = (self.pos[0] - 1, self.pos[1])
                
                self.model.grid.move_agent(self, self.nextPosition)

    def onEdge(self):
        if len(self.currPosiblePositions) == 2:
            return True

    def whatEdge(self):
        if (self.pos[0] == 0) and (self.pos[1] == 0):
            return "left_bottom"
        elif (self.pos[0] == 0) and (self.pos[1] == self.model.grid.height - 1):
            return "left_top"
        elif (self.pos[0] == self.model.grid.width - 1) and (self.pos[1] == 0):
            return "right_bottom"
        elif (self.pos[0] == self.model.grid.width - 1 ) and (self.pos[1] == self.model.grid.height - 1):
            return "right_top"

    def onBorder(self):
        if len(self.currPosiblePositions) == 3:
            return True

    def whatBorder(self):
        if (self.pos[0] == 0):
            return "left"
        elif (self.pos[0] == self.model.grid.width - 1):
            return "right"
        elif (self.pos[1] == 0):
            return "bottom"
        elif (self.pos[1] == self.model.grid.height - 1):
            return "top"

    def whatDirImOn(self):
        currAgents = self.model.grid.get_cell_list_contents(self.pos)
        for agent in currAgents:
            if type(agent) is Road:
                return agent.direction
            elif type(agent) is Traffic_Light:
                return "traffic_light"

    def onCorner(self):
        temp = self.model.grid.get_neighbors(self.pos,moore=False, include_center=False, radius = 1)
        for agent in temp:
            if type(agent) is not Road:
                temp.remove(agent)
        if len(temp) == 4:
            return True
        else:
            return False

    # ? GPS function
    # TODO: Implement GPS function (ADVANCED VERSION)
    def get_destination(self, destiny):
        self.roadToFollow = []
        sum = 0
        startPos = self.model.grid.get_cell_list_contents(self.pos)[0]
        endPos = self.model.grid.get_cell_list_contents(destiny)[0]
        newQueue = queue.priotityQueue()
        newQueue.put(0,sum,startPos)
        prevPath = {}

class Traffic_Light(Agent):
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        pass

class Road(Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.occupied = False
        self.direction = direction # ?  Direction of the road [north, south, east, west]

    def step(self):
        pass

class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Obstacle(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
"""
    Agent class for the --------- model.

    Authors:
        - Carlos Alan Gallegos Espindola (A01751117)
        - Paulina Guadalupe Alva Martinez (A01750624)
        - Jorge Rojas Rivas (A01745334)
        - Omar Rodrigo Talavera Becerra (A01752221)

    Date of creation: 15/11/2022
    Last Modification: 15/11/2022
"""


# Imports
from mesa import Model # Base class for model
from Agentes import AspiradoraAgent # Agent class
from mesa.time import RandomActivation # Scheduler
from mesa.space import MultiGrid # Grid class
from mesa.datacollection import DataCollector # Data collector
import time # Time library for countdown timer

class ModeloRoomba(Model):
    """ Model Class for the Roomba Simulation initializing the model and the agents.

    Methods:
        step: Advance the model by one step.
        current_trashes: Get the number of trashes in the grid.
        timer: Get the time left in the simulation.
    
    """

    def __init__(self, numberOfAgents, numberOfTrashes, width, height, seconds):
        """Initialize a new Roomba Model.
        
        Args:
            numberOfAgents: Number of Roombas in the simulation. (int)
            numberOfTrashes: Number of Trashes in the simulation. (int)
            width: Width of the grid. (int)
            height: Height of the grid. (int)
            seconds: Number of seconds to run the simulation. (int)
            
        Returns:
            None
        """
        self.num_agents = numberOfAgents
        self.num_trashes = numberOfTrashes
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.seconds = seconds
        spaces = self.grid.width * self.grid.height
        rspaces = list(range(spaces))
        rspaces.remove(1) #R: para que es esto?

        # Create Roombas
        for i in range(self.num_agents):
            a = AspiradoraAgent(i, self, "Roomba")
            self.schedule.add(a)

            # Start them on position (1, 1)
            x = 1
            y = 1
            self.grid.place_agent(a, (x, y))

        # Create Trashes
        for i in range(20,20+self.num_trashes):
            b = AspiradoraAgent(i, self,"Basura")
            self.schedule.add(b)
            
            # Add the agent to a random grid cell
            place = self.random.choice(rspaces)
            rspaces.remove(place)
            place = [int(x) for x in str(place)]
            if len (place) <= 1:
                x = int(place[0])
                y = int(place[0])
            else:
                x = int(place[0])
                y = int(place[1])
            self.grid.place_agent(b, (x, y))
            
        self.datacollector_currents = DataCollector(
        {
            "Trashes": ModeloRoomba.current_trashes,
            "Time": ModeloRoomba.timer,
        }
        )

    def step(self):
        """Advance the model by one step.
        
        Args:
            None
            
        Returns:
            None
        """
        self.schedule.step()
        self.datacollector_currents.collect(self)
        if ModeloRoomba.current_trashes(self) == 0 or self.seconds == 0:
            self.running = False

    @staticmethod
    def current_trashes(model) -> int:
        """ Return the total number of trashes 

        Args:
            model(AspiradoraModel)

        Returns: 
            int: Number of Trashes
        """
        return sum([1 for agent in model.schedule.agents if agent.type == "Basura"]) 

    @staticmethod
    def timer(self):
        """ Return the number of seconds left in the simulation

        Args:
            self(ModeloRoomba)

        Returns:
            int: Number of seconds left in the simulation
        """
        while self.seconds:
            mins, secs = divmod(self.seconds, 60)
            timeFormat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeFormat, end="\r")
            time.sleep(1)
            self.seconds -= 1
            return self.seconds 
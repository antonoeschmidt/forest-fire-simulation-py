from drone.drone import drone
from uuid import uuid4
class base_station():
    
    def __init__(self, drones: list(drone), location: tuple(int,int), fire):
        self.number_of_drones = drones
        self.drones = []
        self.location = location
        self.id = str(uuid4())
        self.fire = fire

    ## dispatches a drone 
    def dispatch_drone(self, destination):
        drone.destination = destination
    
    # The drone gets a new location when it gets close enough to the fire to drop it in the next couple of steps.
    def determine_water_drop_location(self, drone):
        drone.desination = (1,1)
        pass
    
    # step has multiple things. 
    # 1. It needs to determine which area to dispatch drones to.
    # 2. It needs to determine where dispatched drones need to drop their water.
    def step(self):
        ## if dispatched drones are close enough, they get a drop location
        for drone in self.drones:
            if drone.destination != self.location and drone.getDistance() <= drone.speed * 2:
                self.determine_water_drop_location(drone)
            if drone.location == self.location and drone.destination == self.location:
                self.initial_dispatch(drone)
        
        # other step is dispatch drones
    
    ## dispatches to a generel area
    def initial_dispatch(self, drone):
        pass
    


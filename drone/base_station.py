from drone.drone import drone
from uuid import uuid4
from typing import Tuple
from typing import List

class base_station():
    
    def __init__(self, drones: List[drone], location: Tuple[int, int], forest):
        self.drones = drones
        self.location = location
        self.id = str(uuid4())
        self.forest = forest

    ## dispatches a drone 
    def dispatch_drone(self, destination):
        drone.destination = destination
    
    # The drone gets a new location when it gets close enough to the fire to drop it in the next couple of steps.
    def determine_water_drop_location(self, drones: List[drone]):
        counter = 0
        #print("len")
        #print(len(drones))
        for i in range(len(self.forest.grid)):
            if len(drones) > counter:
                cell = self.forest.grid[i]
                if cell.fire > 1  and cell.hydration < 2:
                    #print(cell.fire)
                    #print(self.forest.xy(i))
                    drones[counter].set_destination(self.forest.xy(i))
                    counter += 1
    
    def ignited(self, index):
        #print("ignited")
        print(self.forest.grid[index])
        pass
        #self.grid[index] = self.grid[index].factory(fire=1)

    # step has multiple things. 
    # 1. It needs to determine which area to dispatch drones to.
    # 2. It needs to determine where dispatched drones need to drop their water.
    def step(self):
        ## if dispatched drones are close enough, they get a drop location
        valid_drones = []
        for drone in self.drones:
            drone.step()
            #print(drone.position)
            if drone.has_reached_destination() and drone.has_water:
                drone.drop_water()
                #index = drone.location(0) * self.forest.rows + drone.location(1)
                index = self.forest.rows * drone.position[0] + drone.position[1]
               
                #self.forest.grid[index].gotWater = True
                self.forest.grid[index] = self.forest.grid[index].factory(hydration=5, fire = 0)
                
            #elif drone.position != self.location and drone.get_distance() <= drone.speed * 2:
                #self.determine_water_drop_location(drone)
                #valid_drones.append(drone)
            elif drone.position == self.location:
                
                valid_drones.append(drone)
            
            self.determine_water_drop_location(valid_drones)
        # other step is dispatch drones
    
    ## dispatches to a generel area
    def initial_dispatch(self, drone):
        pass
    


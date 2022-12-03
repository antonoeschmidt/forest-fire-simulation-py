from typing import Tuple, List
import sys
from bresenham import bresenham

from ca.cellular_automaton import CellularAutomaton
from drone.fire_coordinate import Coordinate
from drone.fire_state import DroneState
from drone.fire_drone import FireDrone


class DroneSettings(object):

    def __init__(self, drone_speed: int, drone_base_location: Coordinate, number_of_drones: int, wind: Tuple[int, int], **kwargs):
        self.number_of_drones = number_of_drones
        self.location = drone_base_location
        self.drone_speed = drone_speed
        self.wind = wind


class FireInformation(object):
    """Information holder for fires
    """

    def __init__(self, location: Coordinate, fire: int):
        self.location = location
        self.fire = fire

    def __eq__(self, other):
        if isinstance(other, FireInformation):
            return self.fire == other.fire and self.location == other.location
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, FireInformation):
            return self.fire > other.fire
        return False

    def __lt__(self, other):
        return not self.__gt__(other)


class DroneControllerThree(object):
    """Controls and dispatch drones
    """

    def __init__(self, forest: CellularAutomaton, settings: DroneSettings):
        """Creates a new drone controller
        """
        self.location = Coordinate(settings.location['x'], settings.location['y'])
        self.number_of_drones = settings.number_of_drones
        self.drones = [FireDrone(x, settings.drone_speed, self.location.x, self.location.y) for x in
                       range(self.number_of_drones)]
        self.targets: List[Coordinate] = []
        self.forest = forest
        self.targets: List[Coordinate] = []
        self.wind = settings.wind

    def step(self) -> None:
        """Updating all drones respectively

        @return: None
        """
        fires = self.find_fires()
        fire_iterator = iter(fires)

        for drone in self.drones:
            if DroneState.IDLE == drone.state:
                if len(fires) > 0:
                    try:
                        self.assign_fire_to_drone(drone, next(fire_iterator))
                    except StopIteration:
                        fire_iterator = iter(fires)
                        self.assign_fire_to_drone(drone, next(fire_iterator))
                    drone.advance()
                continue

            if not drone.reached_target():
                self.reassign_target(drone, fires)

                drone.advance()
                continue

            if DroneState.REFILLING == drone.state:
                if len(fires) > 0:
                    try:
                        self.assign_fire_to_drone(drone, next(fire_iterator))
                    except StopIteration:
                        fire_iterator = iter(fires)
                        self.assign_fire_to_drone(drone, next(fire_iterator))
                else:
                    drone.set_location(Coordinate(self.location.x, self.location.y))
                    drone.state = DroneState.IDLE

            elif DroneState.FIRE_FIGHTING == drone.state:
                self.reassign_target(drone, fires)
                if drone.target.distance(drone.position) > drone.speed:
                    # not yet reached target
                    continue

                self.forest.drop_water(drone.target.x, drone.target.y, 100)
                self.targets.remove(drone.target)

                drone.state = DroneState.REFILLING
                drone.set_target(Coordinate(self.location.x, self.location.y))

    def reassign_target(self, drone, fires):
        """Reassigns target if already handled
        """
        d_target = drone.target
        if self.forest.get(d_target.x, d_target.y).burned and len(fires) > 0:
            designated_fire: FireInformation = fires[0]

            for f in fires:
                if f.fire < designated_fire.fire and 4 > f.location.distance(designated_fire.location):
                    designated_fire = f

            self.assign_fire_to_drone(drone, designated_fire)

    def assign_fire_to_drone(self, drone: FireDrone, targeted_fire: FireInformation) -> None:
        """
        """
        if drone.target in self.targets:
            self.targets.remove(drone.target)

        drone.state = DroneState.FIRE_FIGHTING
        drone.set_target(targeted_fire.location)
        self.targets.append(Coordinate(targeted_fire.location.x, targeted_fire.location.y))

    def find_fires(self) -> List[FireInformation]:
        """Find list of fires - the order of importance (FIFO)
        """
   
        fires = []
        any_fire = False
        south, north, east, west = (0,0), (0, self.forest.rows), (0,0), (self.forest.cols,0)

        # Find the furtest south, north, east and west.
        for i, cell in enumerate(self.forest.grid):
            if (not cell.burned) and cell.fire > 0:
                any_fire = True
                x, y = self.forest.xy(i)
                if y > south[1]:
                    south = (x, y)
                if y < north[1]:
                    north = (x, y)
                if x > east[0]:
                    east = (x, y)
                if x < west[0]:
                    west = (x, y)

        if not any_fire:
            return []

        west_x = west[0] - 1 if west[0]-1 > -1 else west[0]
        east_x = east[0] + 1 if east[0]+1 < self.forest.cols else east[0]
        north_y = north[1] - 1 if north[1]-1 > -1 else north[1]
        south_y = south[1] + 1 if south[1]+1 < self.forest.rows else south[1]

        south_to_east = list(bresenham(south[0], south_y, east_x, east[1]))
        east_to_north = list(bresenham(east_x, east[1], north[0], north_y))
        north_to_west = list(bresenham(north[0], north_y, west_x, west[1]))
        west_to_south = list(bresenham(west_x, west[1], south[0], south_y))

        print("south_to_east", south_to_east)
        print("east_to_north", east_to_north)
        print("north_to_west", north_to_west)
        print("west_to_south", west_to_south)
        ## Now we find the addional based on the wind direction.
        ## So first we have to find the wind
        additional = []
        x_direction, y_direction = "negative", "negative"

        if self.wind[0] > 0:
            x_direction = "positive"
        if self.wind[1] > 0:
            y_direction = "negative"
        
        points
        if x_direction == "positive":
            if y_direction == "positive":
                # west to south we go south, but we also go east
                points = west_to_south
                points + move_east(points, abs(self.wind[0]), self.forest.rows)
                points + move_south(points, abs(self.wind[1]), self.forest.cols)
                
            else:
                # here y is negative
                points = south_to_east
                # we go to east from south, thats north and east.
                points + move_north(points, abs(self.wind[1]))
                points + move_east(points, abs(self.wind[0]), self.forest.rows)
        # now x is negative
        else:
            if y_direction == "positive":
                # north to west means going south and north.
                points = north_to_west
                points + move_south(points, abs(self.wind[1]), self.forest.cols)
                points + move_west(points, abs(self.wind[0]))
            else:
                # here y is negative
                # going north we go from our east point and then north
                points = east_to_north
                points + move_west(points, abs(self.wind[0]))
                points + move_north(points, abs(self.wind[1]))

        # for p in south_to_east:
        #     # we move right, that positive
        #     if self.wind[0] > 0:
        #         for i in range(self.wind[0]):
        #             if p[0] + i < self.forest.cols:
        #                 additional.append((p[0] + i, p[1]))
        #     # now we move up, thats negative
        #     if self.wind[1] < 0:
        #         for i in range(abs(self.wind[1])):
        #             if p[1] - i < -1:
        #                 additional.append((p[0], p[1] - i))
            
        # for p in east_to_north:
        #     # Now we left, that negative
        #     if self.wind[0] < 0:
        #         for i in range(abs(self.wind[0])):
        #             if p[0] - i < -1:
        #                 additional.append((p[0] - i, p[1]))
        #     # move up, thats negative
        #     if self.wind[1] < 0:
        #         for i in range(abs(self.wind[1])):
        #             if p[1] - i < -1:
        #                 additional.append((p[0], p[1] - i))
                    
        # for p in north_to_west:
        #     # now we move left, so it's positive
        #     if self.wind[0] < 0:
        #         for i in range(abs(self.wind[0])):
        #             if p[0] - i < -1:
        #                 additional.append((p[0] - i, p[1]))
        #     # we move down, thats positive
        #     if self.wind[1] > 0:
        #         for i in range(abs(self.wind[1])):
        #             if p[1] + i < self.forest.cols:
        #                 additional.append((p[0], p[1] + i))
        
        # for p in west_to_south:
        #     # we move left, thats positive
        #     if self.wind[0] > 0:
        #         for i in range(self.wind[0]):
        #             if p[0] + i < self.forest.rows:
        #                 additional.append((p[0] + i, p[1]))
        #     # we move down, thats postive.
        #     if self.wind[1] > 0:
        #         for i in range(abs(self.wind[1])):
        #             if p[1] + i < self.forest.cols:
        #                 additional.append((p[0], p[1] + i))
        
        fires = additional #south_to_east + east_to_north + north_to_west + west_to_south + additional

        # Removing duplicates
        fires = [p for p in (set(tuple(i) for i in fires))]
        print(fires)
        
        # TODO: Add width to wind direction
        # TODO: Handle multiple iginition points
        # TODO: Prioritize the width on the wind direction

        return [FireInformation(Coordinate(fire[0], fire[1]), 0) for fire in fires]

def move_south(points, wind_size, max_index):
    additional = []
    for p in points:
            for i in range(wind_size):
                if p[1] + i < max_index:
                    additional.append((p[0], p[1]  + i))
    
    return additional

def move_north(points, wind_size):
    additional = []
    for p in points:
            for i in range(wind_size):
                if p[1] - i > -1:
                    additional.append((p[0], p[1] - i))
    return additional

def move_east(points, wind_size, max_index):
    additional = []
    for p in points:
            for i in range(wind_size):
                if p[0] + i < max_index:
                    additional.append((p[0] + i, p[1]))
    
    return additional

def move_west(points, wind_size):
    additional = []
    for p in points:
            for i in range(wind_size):
                if p[0] - i > -1:
                    additional.append((p[0] - i, p[1]))
    return additional
from typing import List

from ca.cellular_automaton import CellularAutomaton
from drone.fire_coordinate import Coordinate
from drone.fire_state import DroneState
from drone.fire_drone import FireDrone


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


class DroneController(object):
    """Controls and dispatch drones
    """

    def __init__(self, number_of_drones: int, forest: CellularAutomaton, speed: int, location: Coordinate):
        """Creates a new drone controller
        """
        self.number_of_drones = number_of_drones
        self.drones = [FireDrone(x, speed, location.x, location.y) for x in range(self.number_of_drones)]
        self.targets: List[Coordinate] = []
        self.forest = forest
        self.location = location

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
                if drone.rounds_to_target() == 1:
                    # Re-target to closest and most recent fire?
                    pass
                    designated_fire: FireInformation = fires[0]

                    for f in fires:
                        d = drone.position.distance(f.location)
                        if d < 1 and f.fire < designated_fire.fire:
                            designated_fire = f

                    self.targets.remove(drone.target)
                    self.assign_fire_to_drone(drone, designated_fire)
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
                self.forest.drop_water(drone.target.x, drone.target.y, 100)
                self.targets.remove(drone.target)

                drone.state = DroneState.REFILLING
                drone.set_target(Coordinate(self.location.x, self.location.y))

    def assign_fire_to_drone(self, drone: FireDrone, targeted_fire: FireInformation) -> None:
        """
        """
        drone.state = DroneState.FIRE_FIGHTING
        drone.set_target(targeted_fire.location)
        self.targets.append(targeted_fire.location)

    def find_fires(self) -> List[FireInformation]:
        """Find list of fires - the order of importance (FIFO)
        """
        fires = []
        already_drone_en_route: List[FireInformation] = []
        for i, cell in enumerate(self.forest.grid):
            if (not cell.burned) and cell.fire > 0:
                x, y = self.forest.xy(i)
                coord = Coordinate(x, y)
                if coord not in fires:
                    fires.append(FireInformation(coord, cell.fire))
                else:
                    already_drone_en_route.append(FireInformation(coord, cell.fire))

        fires.sort()
        already_drone_en_route.sort()

        fires.extend(already_drone_en_route)

        return fires

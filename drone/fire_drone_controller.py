from typing import List

from ca.cellular_automaton import CellularAutomaton
from drone.fire_coordinate import Coordinate
from drone.fire_state import DroneState
from drone.fire_drone import FireDrone


class DroneSettings(object):

    def __init__(self, drone_speed: int, drone_base_location: Coordinate, number_of_drones: int, **kwargs):
        self.number_of_drones = number_of_drones
        self.location = drone_base_location
        self.drone_speed = drone_speed


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

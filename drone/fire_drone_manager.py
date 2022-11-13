from typing import List

from ca.cellular_automaton import CellularAutomaton
from drone.fire_coordinate import Coordinate
from drone.fire_state import DroneState
from drone.fire_drone import FireDrone


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

        for drone in self.drones:
            if DroneState.IDLE == drone.state:
                if len(fires) > 0:
                    drone.state = DroneState.FIRE_FIGHTING
                    targeted_fire = fires.pop()
                    self.targets.append(targeted_fire)
                    drone.set_target(targeted_fire)

                    drone.advance()
                continue

            if not drone.reached_target():
                drone.advance()
                continue

            if DroneState.REFILLING == drone.state:
                if len(fires) > 0:
                    drone.state = DroneState.FIRE_FIGHTING
                    targeted_fire = fires.pop()
                    self.targets.append(targeted_fire)
                    drone.set_target(targeted_fire)
                else:
                    drone.set_location(Coordinate(self.location.x, self.location.y))
                    drone.state = DroneState.IDLE

            elif DroneState.FIRE_FIGHTING == drone.state:
                self.forest.drop_water(drone.target.x, drone.target.y, 100)
                self.targets.remove(drone.target)

                drone.state = DroneState.REFILLING
                drone.set_target(Coordinate(self.location.x, self.location.y))

    def find_fires(self) -> List[Coordinate]:
        """Find list of fires - the order of importance (FIFO)
        """
        fires = []
        already_drone_en_route: List[Coordinate] = []
        for i, cell in enumerate(self.forest.grid):
            if (not cell.burned) and cell.fire > 0:
                x, y = self.forest.xy(i)
                coord = Coordinate(x, y)
                if coord not in fires:
                    fires.append(coord)
                else:
                    already_drone_en_route.append(coord)
        fires.extend(already_drone_en_route)

        return fires

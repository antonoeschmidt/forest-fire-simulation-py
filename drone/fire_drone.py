import math

from drone.fire_drone_manager import Coordinate, DroneState


class FireDrone(object):
    """A drone. Location, target and knows how to move
    """

    def __init__(self, d_id: int, speed: int, x: int, y: int):
        self.target: Coordinate | None = None
        self.position: Coordinate = Coordinate(x, y)
        self.d_id = d_id
        self.speed = speed
        self.state = DroneState.IDLE

    def set_location(self, location: Coordinate) -> None:
        self.position = Coordinate(location.x, location.y)

    def set_target(self, location: Coordinate) -> None:
        self.target = Coordinate(location.x, location.y)

    def advance(self) -> None:
        """Move the drone closer to the target

        @return: None
        """
        if self.position is None or self.target is None:
            return

        # distance_to_target
        d = math.sqrt(abs(self.position.x - self.target.x) ** 2 + abs(self.position.y - self.target.y) ** 2)

        (xp, yp) = (self.target.x - self.position.x, self.target.y - self.position.y)

        x = abs(self.position.x + xp * (self.speed / d))
        y = abs(self.position.y + yp * (self.speed / d))

        self.position = Coordinate(int(x), int(y))

    def reached_target(self) -> bool:
        """Has the target been reached?

        @return: True if target is reached o.w. False
        """
        if self.position is None or self.target is None:
            return False

        distance_to_target = math.sqrt(
            abs(self.position.x - self.target.x) ** 2 + abs(self.position.y - self.target.y) ** 2)

        if distance_to_target < self.speed:
            return True
        else:
            return False

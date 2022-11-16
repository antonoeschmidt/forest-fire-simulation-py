import math

from drone.fire_drone_controller import Coordinate, DroneState


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

        if d < self.speed:
            self.set_location(self.target)
            return

        (xp, yp) = (self.target.x - self.position.x, self.target.y - self.position.y)

        x = abs(self.position.x + xp * (self.speed / d))
        y = abs(self.position.y + yp * (self.speed / d))

        print()
        print(f'Drone location: ({int(x)}, {int(y)})')
        print(f'Drone target  : ({self.target.x}, {self.target.y})')

        self.position = Coordinate(int(x), int(y))

    def rounds_to_target(self) -> int:
        """Compute the number of rounds needed for this drone to reach its target

        @return: Rounds to target (int): Returns -1 if no location or target is present
        """
        if self.position is None or self.target is None:
            return -1

        distance_to_target = math.sqrt(
            abs(self.position.x - self.target.x) ** 2 + abs(self.position.y - self.target.y) ** 2)
        return int(distance_to_target / self.speed)

    def reached_target(self) -> bool:
        """Has the target been reached?

        @return: True if target is reached o.w. False
        """
        return self.rounds_to_target() == 0

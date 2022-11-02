import math
from drone.base_station import base_station

# The drone class doesn't contain a lot of info. It has some basic methods but nothing too fancy.
class drone():
    
    def __init__(self, capacity: int, base_station: base_station, env):
        self.env = env
        self.speed = 100 # km/h
        self.capacity = capacity # liters of water
        self.recharge_time = 0
        self.range = 999999999
        self.wind_resistance = 0
        self.base_station_id = 0
        self.position = tuple(int, int)
        self.destination = tuple(int, int)
        self.home_base_station = base_station
        self.has_water = True
        self.water_dropped = env.event()

    def reset(self):
        pass
    
    ## pythagoras to get distance.
    def get_distance(self):
        a = math.abs(self.position[0] - self.destination[0])
        b = math.abs(self.position[1] - self.destination[1])
        return math.sqrt(a ** 2 + b ** 2)
    
    ## is at drop destination
    def has_reached_destination(self):
        return self.position == self.destination and self.position != self.home_base_station.location
    
    ## not sure what i have to write
    def drop_water(self):
        self.has_water = False
        self.destination = self.home_base_station.location
        self.env.event()
    
    def reaching_destination_in_next_step(self):
        self.get_distance <= self.speed
    
    


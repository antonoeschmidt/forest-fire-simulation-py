import simpy

from processes.fire import Fire
from processes.forest import Forest

if __name__ == "__main__":
    env = simpy.Environment()
    forest = Forest(6, 6)
    fire = Fire(env, forest.get_cell(2, 2))
    env.process(fire)
    env.run(until=15)

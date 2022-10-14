import simpy

from processes.forest import Forest

def fire(env, forest):
    yield env.timeout(1)
    forest.step()

if __name__ == "__main__":
    env = simpy.Environment()

    forest = Forest(20, 20)

    env.process(fire(env,forest))

    env.run(until=15)

    forest.fire.print()
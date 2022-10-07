from simpy import Environment


class Fire(object):

    def __init__(self, env: Environment, cell):
        self.env = env
        self.tick = env.now
        self.cell = cell
        # Start the run process everytime an instance is created.
        # self.action = env.process(self.burn())

    def run(self):
        """
        Here we want to burn the cell and in the mean time spread the fire

        Spreading the fire could be done by emitting events. E.g., event spread fire at (x,y)
        and if this cell is still burning, then emit that event and if the cells stopped, emit that event
        Then the event is picked up by??
        """
        print("Burning")
        """
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.charge(charge_duration))

            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)
        
    def charge(self, duration):
        yield self.env.timeout(duration)
        """

import simpy as sp
from simpy.resources.resource import *

class Train(object):
    def __init__(self):
        self.name = "train"

class Station(object):
    def __init__(self, env, name, number):
        self.env = env
        self.resource = {'r':Resource(env, 1), 'l':Resource(env, 1)}
        self.timer = {'r':0, 'l':0}
        self.name = name
        self.number = number
        self.shift = 0

    def arrive(self, train, direction, duration):
        # set timer to zero as the train arrives
        self.timer[direction] = 0

        print("train {} arrived at the station {} at {}".format(train.name, self.name, self.env.now))
        with self.resource[direction].request():
            yield self.env.timeout(duration)
        print("train {} leaved the station {} at {}".format(train.name, self.name, self.env.now))

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.resource['r'].count == 0:
                self.timer['r'] += 1
            if self.resource['l'].count == 0:
                self.timer['l'] += 1

            print("at {} timer is {}".format(self.env.now, self.timer))


def troll_station(station, env):
    yield env.timeout(5)
    yield env.process(station.arrive(Train(), 'r', 5))
    yield env.timeout(3)
    yield env.process(station.arrive(Train(), 'l', 3))

if __name__ == '__main__':
    # t = Station()
    env = sp.RealtimeEnvironment(1)
    station = Station(env, "VG", 1)

    env.process(station.run())
    env.process(troll_station(station, env))

    env.run(until=20)

    print("hey")
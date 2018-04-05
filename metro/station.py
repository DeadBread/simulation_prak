import simpy as sp
from simpy.resources.resource import *

class Train(object):
    def __init__(self, env, number, station, direction):
        self.env = env
        self.number = number
        self.next_station = station
        self.direction = direction

    def drive(self, durs):
        while True:
            go_dur = durs[0]
            wait_dur = durs[1]
            yield self.env.timeout(go_dur)
            print("train {}, arrived to the station {} at {} so {} {}".format(self.number, self.next_station.name, self.env.now, go_dur, wait_dur))
            yield self.env.process(self.next_station.arrive(self, wait_dur))
            print("train {} waited for {} departing at {}".format(self.number, wait_dur, self.env.now))
            self.next_station = self.next_station.next

class Station(object):
    def __init__(self, env, name, number):
        self.env = env
        self.resource = {'r':Resource(env, 1), 'l':Resource(env, 1)}
        self.timer = {'r':0, 'l':0}
        self.name = name
        self.number = number
        self.shift = 0
        self.next = None

    def arrive(self, train, duration):

        direction = train.direction
        # set timer to zero as the train arrives
        self.timer[direction] = 0

        print("train {} arrived at the station {} at {} ".format(train.number, self.number, self.env.now))
        with self.resource[direction].request():
            yield self.env.timeout(duration)
        print("train {} leaved the station {} at {}".format(train.number, self.number, self.env.now))

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.resource['r'].count == 0:
                self.timer['r'] += 1
            if self.resource['l'].count == 0:
                self.timer['l'] += 1

            # print("at {} timer is {}".format(self.env.now, self.timer))


def troll_station(station, env):
    yield env.timeout(5)
    yield env.process(station.arrive(Train(), 'r', 5))
    yield env.timeout(3)
    yield env.process(station.arrive(Train(), 'l', 3))


def troll_train(env):
    ln = 10
    stations = []
    for i in range(ln):
        stations.append(Station(env, str(i), i))

    for i in range(ln - 1):
        env.process(stations[i].run())
        stations[i].next = stations[i+1]
    stations[-1].next = stations[0]

    train = Train(env, 1, stations[0], 'r')

    go_int = 3
    wait_int = 3
    list = [go_int, wait_int]

    env.process(train.drive(list))
    env.process(real_troll_train(env, list))
    env.run(until=20)


def real_troll_train(env,list):
    yield env.timeout(5)
    list[1] = 2
    yield env.timeout(5)
    list[0] = 0
    yield env.timeout(5)
    list[1] = 5


if __name__ == '__main__':
    # t = Station()
    env = sp.RealtimeEnvironment()
    troll_train(env)
    # station = Station(env, "VG", 1)
    #
    # env.process(station.run())
    # env.process(troll_station(station, env))
    #
    # env.run(until=20)

    print("hey")
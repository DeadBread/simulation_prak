import simpy as sp
from simpy.resources.resource import *
from metro import graphs
from PyQt5 import QtCore

class Train(object):
    def __init__(self, env, scene, number, station, direction):
        self.env = env
        self.number = number
        self.next_station = station
        self.direction = direction

        self.above = 55

        self.gr = graphs.GraphTrain(100, 300 + self.above)
        self.gr.setAcceptHoverEvents(True)
        self.gr.setAcceptDrops(True)
        scene.addItem(self.gr)


    def drive(self, durs):
        while True:
            go_dur = durs[0]
            wait_dur = durs[1]
            yield self.env.timeout(go_dur)
            print("train {}, arrived to the station {} at {} so {} {}".format(self.number, self.next_station.name, self.env.now, go_dur, wait_dur))
            print("current pos", self.gr.pos())
            yield self.env.process(self.next_station.accept(self, wait_dur))
            print("train {} waited for {} departing at {} to {}".format(self.number, wait_dur, self.env.now, self.next_station.next[self.direction].name))
            self.next_station = self.next_station.next[self.direction]

    def move(self, dist):
        print("\n\n", self.gr.pos())
        if self.direction == 'r':
            # self.gr.setPos(self.gr.pos() + QtCore.QPointF(dist, 1))
            self.gr.moveBy(dist, 0.)
        else:
            self.gr.moveBy(- dist, 0.)
        print(self.gr.pos(), "\n\n")

    def jump(self):
        if self.direction == 'r':
            self.direction = 'l'
            self.gr.moveBy(0., -50 - 2 * 30)
        else:
            self.direction = 'r'
            self.gr.moveBy(0., 50 + 2 * 30)

        print("changed direction! next is ", self.next_station.next[self.direction].name)


class Station(object):
    def __init__(self, env, scene, n_stations, name, number):
        self.env = env
        self.resource = {'r': Resource(env, 1), 'l':Resource(env, 1)}
        self.timer = {'r': 0, 'l': 0}
        self.name = name
        self.number = number

        self.dist = 1000 / n_stations
        self.shift = 100 + self.dist * number
        self.next = dict()

        self.gr = graphs.GraphStation(self.shift, 300)
        self.gr.setAcceptHoverEvents(True)
        self.gr.setAcceptDrops(True)
        scene.addItem(self.gr)

    def accept(self, train, duration):

        direction = train.direction
        # set timer to zero as the train arrives
        self.timer[direction] = 0

        train.move(self.dist)

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

class TerminalStation(Station):
    # only difference with ordinary station is that it turns the train around
    def accept(self, train, duration):
        res = super(TerminalStation, self).accept(train, duration)
        yield self.env.process(res)
        train.jump()


class Branch(object):
    def __init__(self, env, scene, s_num, t_num):

        self.go_dur = 5
        self.wait_dur = 1
        self.interval = 3

        self.env = env
        self.scene = scene

        self.trains = []
        self.stations = [TerminalStation(self.env, scene, s_num, "Саларьево", 0)]

        for i in range(s_num - 2):
            self.stations.append(Station(self.env, scene, s_num, str(i+1), i+1))

        self.stations.append(TerminalStation(self.env, scene, s_num, "Rhz", 0))

        for i in range(s_num-1):
            self.stations[i].next['r'] = self.stations[i+1]

        for i in range(1, s_num):
            self.stations[i].next['l'] = self.stations[i-1]

        # print(self.stations[s_num-1].next['l'].name)

        #     self.stations[i].next['r'] = self.stations[i+1]
        #     self.stations[i].next['l'] = self.stations[i-1]
        # self.stations[0].next['r'] = self.stations[1]
        # self.stations.append(TerminalStation(self.env,scene, s_num, "Бульвар Рокосовского", s_num-1))
        # self.stations[s_num-2].next['r'] = self.stations[s_num-1]
        # self.stations[s_num - 1].next['l'] = self.stations[s_num-2]
        # self.stations[s_num-1].next['r'] = self.stations[0]

        self.gr_branch = graphs.GraphBranch(scene, self.stations)

        for i in range(t_num):
            self.trains.append(Train(self.env, scene, i, self.stations[1], 'r'))

    def go(self):
        for station in self.stations:
            self.env.process(station.run())
        start_timeout = self.wait_dur + self.go_dur + self.interval
        for train in self.trains:
            self.env.process(train.drive([self.go_dur, self.wait_dur]))
            yield self.env.timeout(start_timeout)




def troll_station(station, env):
    yield env.timeout(5)
    yield env.process(station.accept(Train(), 'r', 5))
    yield env.timeout(3)
    yield env.process(station.accept(Train(), 'l', 3))


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



    # branch = Branch(env, 10, 5)

    print("here")

    # env.process(branch.go())
    env.run()

    # station = Station(env, "VG", 1)
    #
    # env.process(station.run())
    # env.process(troll_station(station, env))
    #
    # env.run(until=20)

    print("hey")
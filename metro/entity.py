import simpy as sp
from simpy.resources.resource import *
from metro import graphs, schedule
from math import ceil, floor
from PyQt5 import QtCore

class Train(object):
    def __init__(self, env, canvas, number, station, direction):
        self.env = env
        self.number = number
        self.next_station = station
        self.direction = direction

        self.canvas = canvas

        self.delay = 0

        # self.above = 55

        self.graph_id = graphs.TrainBuilder.build(self.canvas, station.next[self.rev_direction()], direction)


    def rev_direction(self):
        if self.direction == 'r':
            return 'l'
        else:
            return 'r'


    def drive(self, schedule):
        while True:
            go_dur = schedule.go_interval
            wait_dur = schedule.wait_interval

            # fixing delay:
            if go_dur - self.delay >= (go_dur/1.5):
                go_dur -= self.delay
                self.delay = 0
            elif wait_dur - (self.delay - (go_dur - go_dur/1.5)) >= 1:
                wait_dur -= (self.delay - (go_dur - go_dur/1.5))
                go_dur /= 1.5
                print("wow!", go_dur, wait_dur, self.delay)
                print(wait_dur >= 1)
                self.delay = 0

            else:
                print(self.delay)
                self.delay -= (go_dur - go_dur/1.5)
                self.delay -= wait_dur - 1
                go_dur /= 1.5
                wait_dur = 1

            print(go_dur, wait_dur, self.delay)

            self.delay += schedule.delay()

            # yield self.env.timeout(go_dur)
            yield self.env.process(self.move(go_dur, self.next_station.dist))
            yield self.env.process(self.next_station.accept(self, wait_dur + self.delay))
            self.next_station = self.next_station.next[self.direction]

    def move(self, go_dur, dist):
        if self.direction == 'r':
            dx = dist
        else:
            dx = - dist

        part_dx = dx / go_dur

        for i in range(floor(go_dur)):
            self.canvas.move(self.graph_id, part_dx, 0)
            yield self.env.timeout(1)

        # дробная часть
        if (go_dur % 1 > 0):
            self.canvas.mobe(self.graph_id, part_dx * go_dur % 1, 0)
            yield self.env.timeout(go_dur % 1)


        # self.canvas.move(self.graph_id, dx, 0)

    def turn_around(self):
        if self.direction == 'r':
            self.direction = 'l'
            dy = -50 - 2 * 30 - 20
        else:
            self.direction = 'r'
            dy = 50 + 2 * 30 + 20
        self.canvas.move(self.graph_id, 0, dy)


class Station(object):
    def __init__(self, env, canvas, n_stations, name, number):
        self.env = env
        self.resource = {'r': Resource(env, 1), 'l':Resource(env, 1)}
        self.timer = {'r': 0, 'l': 0}
        self.name = name
        self.number = number

        self.dist = 1000 / n_stations
        self.shift = 100 + self.dist * number
        self.next = dict()

        self.canvas = canvas
        self.graph_id = graphs.StationBuilder.build(self.canvas, self.shift)

    def accept(self, train, duration):

        direction = train.direction
        # set timer to zero as the train arrives
        self.timer[direction] = 0

        # print("train {} arrived at the station {} at {} ".format(train.number, self.number, self.env.now))
        with self.resource[direction].request():
            yield self.env.timeout(duration)
        # print("train {} leaved the station {} at {}".format(train.number, self.number, self.env.now))

    def request(self, dir):
        self.resource[dir].request()

    def release(self, dir):
        self.resource[dir].release()

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.resource['r'].count == 0:
                self.timer['r'] += 1
            if self.resource['l'].count == 0:
                self.timer['l'] += 1


class TerminalStation(Station):
    # only difference with ordinary station is that it turns the train around
    def accept(self, train, duration):
        res = super(TerminalStation, self).accept(train, duration)
        yield self.env.process(res)
        train.turn_around()


class Branch(object):
    def __init__(self, env, canvas, s_num, t_num):

        # self.go_dur = 5
        # self.wait_dur = 1
        # self.interval = 3

        self.schedule = schedule.Schedule(env, s_num, t_num)

        self.env = env
        self.canvas = canvas

        self.trains = []
        self.stations = [TerminalStation(self.env, canvas, s_num, "Саларьево", 0)]

        for i in range(s_num - 2):
            self.stations.append(Station(self.env, canvas, s_num, str(i + 1), i + 1))

        self.stations.append(TerminalStation(self.env, canvas, s_num, "Rhz", s_num - 1))

        print(len(self.stations))

        for i in range(s_num-1):
            self.stations[i].next['r'] = self.stations[i+1]

        for i in range(1, s_num):
            self.stations[i].next['l'] = self.stations[i-1]

        for i in range(t_num):
            self.trains.append(Train(self.env, canvas, i, self.stations[1], 'r'))

    def go(self):
        for station in self.stations:
            self.env.process(station.run())
        start_timeout = self.schedule.initial_delay
        for train in self.trains:
            self.env.process(train.drive(self.schedule))
            yield self.env.timeout(start_timeout)

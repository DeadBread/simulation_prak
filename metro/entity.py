import simpy as sp
from simpy.resources.resource import *
from metro import graphs, schedule
from math import ceil, floor
from PyQt5 import QtCore
from tkinter import StringVar

class Train(object):
    def __init__(self, env, canvas, number, station, direction):
        self.env = env
        self.number = number
        self.next_station = station
        self.direction = direction

        self.canvas = canvas

        self.delay = 0

        self.next_train = None
        self.on_station = False
        self.leaving_at = 0

        # self.above = 55

        self.graph_id = graphs.TrainBuilder.build(self.canvas, station.next[self.rev_direction()], direction, number)
        self.text_id = graphs.TrainBuilder.build_text(self.canvas, station.next[self.rev_direction()], direction, number)

        self.x = 0

        self.driving = False


    def rev_direction(self):
        if self.direction == 'r':
            return 'l'
        else:
            return 'r'


    def drive(self, schedule, next):
        self.driving = True
        self.next_train = next
        while True:
            go_dur = schedule.go_interval
            wait_dur = schedule.wait_interval

            # fixing delay:
            if go_dur - self.delay >= go_dur/1.5:
                go_dur -= self.delay
                self.delay = 0
            elif wait_dur - (self.delay - (go_dur - go_dur/1.5)) >= 1:
                wait_dur -= (self.delay - (go_dur - go_dur/1.5))
                go_dur /= 1.5
                # print("wow!", go_dur, wait_dur, self.delay)
                print(wait_dur >= 1)
                self.delay = 0

            else:
                # print(self.delay)
                self.delay -= (go_dur - go_dur/1.5)
                self.delay -= wait_dur - 1
                go_dur /= 1.5
                wait_dur = 1

            # print(go_dur, wait_dur, self.delay)

            # self.delay += schedule.delay()

            # yield self.env.timeout(go_dur)
            yield self.env.process(self.move(go_dur, self.next_station.dist))

            yield self.env.process(self.wait_on_station(wait_dur, schedule.delay(), schedule.go_interval))

    def wait_on_station(self, wait_dur, tmp_del, go_dur):

        self.on_station = True

        # tmp_del =
        self.leaving_at = self.env.now + wait_dur + tmp_del

        with self.next_station.resource[self.direction].request() as req:

            yield req

            self.canvas.move(self.graph_id, self.part_dx * 2, 0)
            self.canvas.move(self.text_id, self.part_dx * 2, 0)

            self.delay += tmp_del

            print("train ", self.number, "arrived at", self.env.now, " to", self.next_station.number, "dir", self.direction)

            yield self.env.timeout(wait_dur + tmp_del)
            # yield self.env.process(self.next_station.accept(self, wait_dur + self.delay))

            extra_wait = 0

            self.next_station.register_train(wait_dur, self.delay, self.direction)
            # if self.next_train.next_station is not None:

            while self.next_train.driving and (self.next_train.next_station == self.next_station.next[self.direction]
                        or self.next_train.next_station == self.next_station and self.next_station.is_terminal)\
                    and self.next_train.on_station\
                    and self.direction == self.next_train.direction:

                # self.delay += 1
                yield self.env.timeout(1)

                print ("extra first case", self.number, extra_wait)
            while self.next_train.driving and (self.next_train.next_station == self.next_station \
                    or self.next_train.next_station == self.next_station.next[self.direction]):
                print(self.number, self.next_train.number)

                # self.delay += 1
                yield self.env.timeout(1)
                print("extra second case", self.number, extra_wait)

            print(self.number, self.next_train.number)

            # print("self.next_train.leaving_at, self.env.now, extra_wait = ", extra_wait, self.next_train.leaving_at, self.env.now)

            yield self.env.timeout(extra_wait)

            if self.next_station.is_terminal:
                self.turn_around()
                self.leaving_at = wait_dur
                yield self.env.timeout(wait_dur)
                wait_dur *= 2

            self.on_station = False
            self.leaving_at = 0

            print("train ", self.number, "free at", self.env.now, "of", self.next_station.number,  "dir", self.direction)


        self.next_station = self.next_station.next[self.direction]


            # self.next_station.resource[self.direction].release(req)

    def move(self, go_dur, dist):
        if self.direction == 'r':
            dx = dist
        else:
            dx = - dist

        self.part_dx = dx / go_dur

        for i in range(floor(go_dur) - 2):
            self.canvas.move(self.graph_id, self.part_dx, 0)
            self.canvas.move(self.text_id, self.part_dx, 0)
            yield self.env.timeout(1)

        # дробная часть
        if go_dur % 1 > 0:
            self.canvas.move(self.graph_id, self.part_dx * go_dur % 1, 0)
            self.canvas.move(self.text_id, self.part_dx * go_dur % 1, 0)
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
        self.canvas.move(self.text_id, 0, dy)


class Station(object):
    def __init__(self, env, canvas, n_stations, name, number):
        self.env = env
        self.resource = {'r': Resource(env, 1), 'l':Resource(env, 1)}
        self.timer = {'r': 0, 'l': 0}
        self.name = name
        self.number = number

        self.dist = 1300 / n_stations
        self.shift = 50 + self.dist * number
        self.next = {'l':None, 'r':None}

        self.is_terminal = False

        self.canvas = canvas
        self.graph_id = graphs.StationBuilder.build(self.canvas, self.shift)
        self.text_id = graphs.StationBuilder.build_text(self.canvas, self.shift, number)

        self.wait_dur = {'r':0, 'l':0}
        self.delay = {'r': 0, 'l': 0}

        self.label_text = {'r': StringVar(), 'l':  StringVar()}

        self.label = dict()
        self.label['r'] = graphs.StationBuilder.build_label_r(canvas, self.shift, self.label_text['r'])
        self.label['l'] = graphs.StationBuilder.build_label_l(canvas, self.shift, self.label_text['l'])

    def update_label(self, dir):
        self.canvas.itemconfig(self.label[dir],
                       text="time: " + str(self.env.now) + '\n' \
                    + "since last: " + str(self.timer[dir]) + '\n' \
                    + "wait_dur: " + str(self.wait_dur[dir]) + '\n'\
                    + "delay: " + str(self.delay[dir]) + '\n')
        # print("here")

    def register_train(self, wait_dur, delay, dir):
        self.wait_dur[dir] = wait_dur
        self.delay[dir] = delay
        self.timer[dir] = 0


    # def accept(self, train, duration):
    #
    #     direction = train.direction
    #     # set timer to zero as the train arrives
    #     self.timer[direction] = 0
    #
    #     # print("train ", train.number, "req at", self.env.now, "dir", direction)
    #     with self.resource[direction].request():
    #         yield self.env.timeout(duration)
    #     # print("train ", train.number, "free at", self.env.now, "dir", direction)

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.resource['r'].count == 0:
                self.timer['r'] += 1
            if self.resource['l'].count == 0:
                self.timer['l'] += 1

            self.update_label('r')
            self.update_label('l')


class TerminalStation(Station):
    # only difference with ordinary station is that it turns the train around
    def __init__(self, env, canvas, n_stations, name, number):
        super(TerminalStation, self).__init__(env, canvas, n_stations, name, number)
        self.is_terminal = True
    def accept(self, train, duration):
        res = super(TerminalStation, self).accept(train, duration)
        yield self.env.process(res)


class Branch(object):
    def __init__(self, env, canvas, params):

        self.schedule = schedule.Schedule(env, params)

        s_num = params.num_stations.get()
        t_num = params.num_trains.get()

        self.env = env
        self.canvas = canvas

        self.trains = []
        self.stations = [TerminalStation(self.env, canvas, s_num, "0", 0)]

        for i in range(s_num - 2):
            self.stations.append(Station(self.env, canvas, s_num, str(i + 1), i + 1))

        self.stations.append(TerminalStation(self.env, canvas, s_num, "x", s_num - 1))

        print(len(self.stations))

        for i in range(s_num-1):
            self.stations[i].next['r'] = self.stations[i+1]

        for i in range(1, s_num):
            self.stations[i].next['l'] = self.stations[i-1]

        for i in range(t_num):
            self.trains.append(Train(self.env, canvas, i, self.stations[1], 'r'))

        for i in range(t_num - 1):
            self.trains[i].next_train = self.trains[i+1]
        self.trains[-1].next_train = self.trains[0]

    def go(self):
        for station in self.stations:
            self.env.process(station.run())
        start_timeout = self.schedule.initial_delay
        for i, train in enumerate(self.trains):
            self.env.process(train.drive(self.schedule, self.trains[i-1]))
            yield self.env.timeout(start_timeout)

import sys
import simpy as sp
from metro import graphs, entity
from PyQt5.QtCore import QThread
from tkinter import *
import time






class SimulateTread(QThread):

    def __init__(self, env, exit):
        QThread.__init__(self)
        self.env = env
        self.exit = exit

    def __del__(self):
        self.wait()

    def run(self):
        self.env.run(until=self.exit)


class MyNumEntry():
    def __init__(self, root, tv):
        vcmd = (root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.text1 = Entry(root, textvariable = tv, validate='key', validatecommand=vcmd)
        self.text1.pack()
        self.text1.focus()

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if action != '1':
            return True
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


class Params(object):
    def __init__(self,
                    root,
                    speed = 10.,
                    num_trains = 8,
                    num_stations = 10,
                    stay_time = 3,
                    go_time = 15):
        self.speed = DoubleVar(root)
        self.num_trains = IntVar(root)
        self.num_stations = IntVar(root)
        self.stay_time = DoubleVar(root)
        self.go_time = DoubleVar(root)

        try:
            speed = float(speed)
            if (speed < 0.):
                speed = 1.
            if (speed > 20.):
                speed = 20.
        except:
            speed = 5.

        try:
            num_stations = int(num_stations)
            if num_stations > 14:
                num_stations = 14
            if num_stations < 3:
                num_stations = 3
        except:
            num_stations = 10

        try:
            num_trains = int(num_trains)
            if num_trains > num_stations - 2:
                num_trains = num_stations - 2
            if num_trains < 1:
                num_trains = 1
        except:
            num_trains = int(num_stations / 2)

        try:
            stay_time = float(stay_time)
            if stay_time > 15:
                stay_time = 15
            if stay_time < 1:
                stay_time = 1
        except:
            stay_time = 3

        try:
            go_time = float(go_time)
            if go_time > 30:
                go_time = 30
            if go_time < 5:
                go_time = 5
        except:
            go_time = 15


        print(speed, num_stations, num_trains, stay_time, go_time)


        self.speed.set(speed)
        self.num_trains.set(num_trains)
        self.num_stations.set(num_stations)
        self.stay_time.set(stay_time)
        self.go_time.set(go_time)



if __name__ == '__main__':
    root = Tk()

    # root.resizable(width=False, height=False)
    # root.maxsize(width=666, height=666)

    canvas = Canvas(root, width=1500, height=350)

    # params = Params(root)

    canvas.pack()

    var = IntVar()

    start_b = Button(root, text='start', command = lambda: var.set(1))
    start_b.pack()



    par_speed = StringVar()
    par_speed.set('speed')

    par_num_trains = StringVar()
    par_num_trains.set('number of train')

    par_num_stations = StringVar()
    par_num_stations.set('number of stations')

    par_stay_time = StringVar()
    par_stay_time.set('stay interval')

    par_stay_time = StringVar()
    par_stay_time.set('move interval')


    MyNumEntry(root, par_speed)
    MyNumEntry(root, par_num_trains)
    MyNumEntry(root, par_num_stations)
    MyNumEntry(root, par_stay_time)
    MyNumEntry(root, par_stay_time)


    start_b.wait_variable(var)


    params = Params(root, par_speed.get(), par_num_trains.get(), par_num_stations.get(), par_stay_time.get(), par_stay_time.get() )

    env = sp.RealtimeEnvironment(0, 1 / params.speed.get(), strict=False)
    branch = entity.Branch(env, canvas, params)

    exit = env.event()
    exit_b = Button(root, text="exit", command = lambda: exit.succeed() and sys.exit(0))
    exit_b.pack()

    env.process(branch.go())
    t = SimulateTread(env, exit)
    t.start()

    root.mainloop()

    sys.exit(0)

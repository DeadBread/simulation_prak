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

    params = Params(root)

    canvas.pack()


    so_l = Label(text="speed")
    so_l.pack()
    sp_m = OptionMenu(root, params.speed, 1, 2, 5, 10, 20)
    sp_m.place(x=650, y=370, bordermode='inside', in_=root)

    trn_m = OptionMenu(root, params.num_trains, 1, 2, 3, 5, 7, 10)
    trn_m.pack()
    trn_m.place(x=650, y=400)

    sn_m = OptionMenu(root, params.num_stations, 3, 5, 7, 9, 10, 12)
    sn_m.pack()
    sn_m.place(x=650, y=430)

    st_m = OptionMenu(root, params.stay_time, 1, 2, 3, 5, 7)
    st_m.pack()
    st_m.place(x=650, y=460)

    gt_m = OptionMenu(root,  params.go_time, 3, 5, 7, 10, 12, 15, 20)
    gt_m.pack()
    gt_m.place(x=650, y=490)

    time.sleep(4)

    env = sp.RealtimeEnvironment(0, 0.2, strict=False)
    branch = entity.Branch(env, canvas, params)

    exit = env.event()
    env.process(branch.go())
    t = SimulateTread(env, exit)

    start_b = Button(root, text='start', command = SimulateTread(env, exit).start)
    start_b.pack()

    exit_b = Button(root, text="exit", command=exit.succeed)
    exit_b.pack()



    # t.start()

    root.mainloop()

    sys.exit(0)

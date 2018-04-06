import sys
import simpy as sp
from metro import graphs, station
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from tkinter import *



class SimulateTread(QtCore.QThread):

    def __init__(self, env):
        QtCore.QThread.__init__(self)
        self.env = env

    def __del__(self):
        self.wait()

    def run(self):
        self.env.run()




if __name__ == '__main__':
    root = Tk()

    canvas = Canvas(root, width=1200, height=500)
    canvas.pack()

    env = sp.RealtimeEnvironment(0, 0.1)

    branch = station.Branch(env, canvas, 10, 1)

    # w.
    # w.show()


    env.process(branch.go())
    t = SimulateTread(env)
    t.start()

    root.mainloop()

    # print("here")
    # env.run()

    sys.exit(0)


# from tkinter import *
# from random import randint
#
# root = Tk()
#
# canvas = Canvas(root, width=1200, height=500)
# canvas.pack()
#
#
#
# # int = graphs.TrainBuilder.build(canvas, station.Station(0, 0, 10, 'name', 7), 'r')
# # print(int)
#
# # for i in range(100):
# #     x, y = randint(0, 1000-1), randint(0, 500-1)
# #     canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
#
# root.mainloop()
#

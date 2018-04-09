import sys
import simpy as sp
from metro import graphs, entity
from PyQt5.QtCore import QThread
from tkinter import *



class SimulateTread(QThread):

    def __init__(self, env):
        QThread.__init__(self)
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

    # env = sp.Environment()
    branch = entity.Branch(env, canvas, 12, 10)

    env.process(branch.go())
    t = SimulateTread(env)
    t.start()

    root.mainloop()

    sys.exit(0)

import sys
import simpy as sp
from metro import graphs, station
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore



class SimulateTread(QtCore.QThread):

    def __init__(self, env):
        QtCore.QThread.__init__(self)
        self.env = env

    def __del__(self):
        self.wait()

    def run(self):
        self.env.run()




# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#
#     scene = QGraphicsScene()
#
#     # w = QWidget()
#     # w.resize(250, 150)
#     # w.move(300, 300)
#     # w.setWindowTitle('Simple')
#     # t = graphs.GraphTrain()
#     # t.setAcceptHoverEvents(True)
#     # t.setAcceptDrops(True)
#     #
#     # ts = graphs.GraphStation()
#     # ts.setAcceptHoverEvents(True)
#     # ts.setAcceptDrops(True)
#
#     env = sp.RealtimeEnvironment(0, 0.1)
#
#     branch = station.Branch(env, scene, 10, 1)
#     new = graphs.GraphBranch(scene, branch.stations)
#
#     # w.
#     # w.show()
#
#     view = QGraphicsView(scene)
#     view.setRenderHint(QtGui.QPainter.Antialiasing)
#     view.resize(200, 100)
#
#     env.process(branch.go())
#     t = SimulateTread(env)
#     t.start()
#
#     view.show()
#
#     app.exec_()
#
#     print("here")
#     # env.run()
#
#     sys.exit(0)


from tkinter import *
from random import randint

root = Tk()

canvas = Canvas(root, width=1200, height=500)
canvas.pack()

def click(event):
    if canvas.find_withtag(CURRENT):
        canvas.itemconfig(CURRENT, fill="blue")
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")

for i in range(100):
    x, y = randint(0, 1000-1), randint(0, 500-1)
    canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")

canvas.bind("<Button-1>", click)

root.mainloop()


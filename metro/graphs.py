from tkinter import *

from functools import partial




# class GraphTrain(QGraphicsEllipseItem):
#     def __init__(self, x, y):
#         QGraphicsEllipseItem.__init__(self, 0, 0, 50, 20,)
#         self.setPos(QPointF(x, y))
#         self.setBrush(QColor(88,245,139))
#
#     def mouseReleaseEvent(self, event):
#         # Do your stuff here.
#         self.setBrush(Qt.red)
#         return QGraphicsEllipseItem.mouseReleaseEvent(self, event)
#
#     def hoverLeaveEvent(self, event):
#         self.setBrush(QColor(88,245,139))
#
#         # Do your stuff here.
#         pass
#
#     def hoverEnterEvent(self, event):
#         self.setBrush(Qt.blue)
#         # Do your stuff here.
#         pass
#
#
# class GraphStation(QGraphicsEllipseItem):
#     def __init__(self, x, y):
#         QGraphicsEllipseItem.__init__(self, x, y, 50, 50,)
#         self.setBrush(Qt.red)
#         self.setPen(QPen(10))
#
#     def mouseReleaseEvent(self, event):
#         # Do your stuff here.
#         self.setBrush(Qt.red)
#         return QGraphicsEllipseItem.mouseReleaseEvent(self, event)
#
#     def hoverLeaveEvent(self, event):
#         self.setBrush(Qt.red)
#
#         # Do your stuff here.
#         pass
#
#     def hoverEnterEvent(self, event):
#         self.setBrush(Qt.blue)
#         # Do your stuff here.
#         pass
#
#


class StationBuilder(object):

    station_radius = 50
    station_height = 300

    color = '#fa7aa8'

    @staticmethod
    def build(canvas, shift):
        x0 = shift
        y0 = 300
        x1 = x0 + StationBuilder.station_radius
        y1 = y0 + StationBuilder.station_radius

        # canvas.bind("<Button-1>", partial(TrainBuilder.click, canvas))

        return canvas.create_oval(x0,y0 ,x1 ,y1, fill=StationBuilder.color)


class TrainBuilder(object):

    station_radius = 50
    above  = 30
    station_height = 300

    length = 50
    height = 20
    color = '#83f3a2'

    # @staticmethod
    # def click(canvas, event):
    #     if canvas.find_withtag(CURRENT):
    #         canvas.itemconfig(CURRENT, fill="blue")
    #         canvas.update_idletasks()
    #         canvas.after(200)
    #         canvas.itemconfig(CURRENT, fill="red")

    @staticmethod
    def build(canvas, station, direction):
        x0 = station.shift
        if (direction == 'r'):
            y0 = TrainBuilder.station_height + TrainBuilder.station_radius + TrainBuilder.above
        else:
            y0 = TrainBuilder.station_height - TrainBuilder.station_radius - TrainBuilder.above - TrainBuilder.height

        x1 = x0 + TrainBuilder.length
        y1 = y0 + TrainBuilder.height

        # canvas.bind("<Button-1>", partial(TrainBuilder.click, canvas))

        return canvas.create_oval(x0,y0 ,x1 ,y1, fill=TrainBuilder.color)


#
# class GraphBranch:
#     def __init__(self, canvas, stations):
#         self.train_picts = dict()
#         self.station_picts = dict()
#
#         shift = 100
#         N = len(stations)
#         dist = 1000. / N
#
#         for i, station in enumerate(stations):
#             tmp = GraphStation(shift + i * dist, 300)
#             tmp.setAcceptHoverEvents(True)
#             tmp.setAcceptDrops(True)
#             self.station_picts[station] = tmp
#             scene.addItem(self.station_picts[station])




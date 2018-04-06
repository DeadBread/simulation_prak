from tkinter import *




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
# class GraphBranch:
#     def __init__(self, scene, stations):
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




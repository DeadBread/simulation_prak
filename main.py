import sys
import metro
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt


class GraphTrain(QGraphicsEllipseItem):
    def __init__(self):
        QGraphicsEllipseItem.__init__(self, 355, 280, 70, 40,)
        self.setBrush(QColor(88,245,139))

    def mouseReleaseEvent(self, event):
        # Do your stuff here.
        self.setBrush(Qt.red)
        return QGraphicsEllipseItem.mouseReleaseEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QColor(88,245,139))

        # Do your stuff here.
        pass

    def hoverEnterEvent(self, event):
        self.setBrush(Qt.blue)
        # Do your stuff here.
        pass


class GraphStation(QGraphicsEllipseItem):
    def __init__(self):
        QGraphicsEllipseItem.__init__(self, 600, 280, 50, 50,)
        self.setBrush(Qt.red)
        self.setPen(QPen(10))

    def mouseReleaseEvent(self, event):
        # Do your stuff here.
        self.setBrush(Qt.red)
        return QGraphicsEllipseItem.mouseReleaseEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setBrush(Qt.red)

        # Do your stuff here.
        pass

    def hoverEnterEvent(self, event):
        self.setBrush(Qt.blue)
        # Do your stuff here.
        pass



if __name__ == '__main__':

    app = QApplication(sys.argv)

    scene = QGraphicsScene()

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    t = GraphTrain()
    t.setAcceptHoverEvents(True)
    t.setAcceptDrops(True)

    ts = GraphStation()
    ts.setAcceptHoverEvents(True)
    ts.setAcceptDrops(True)

    # w.
    # w.show()

    scene.addItem(t)
    scene.addItem(ts)

    view = QGraphicsView(scene)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.resize(200, 100)

    view.show()

    sys.exit(app.exec_())
from tkinter import *

from functools import partial


COLORS = ['yellow2', 'DarkGoldenrod3', 'IndianRed2',
    'IndianRed3', 'sienna3', 'wheat1', 'chocolate3', 'salmon1', 'orange2', 'tomato4', 'OrangeRed2','pink2',
    'maroon1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2',
    'MediumOrchid4',
    'purple1',
    'MediumPurple3',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']


class StationBuilder(object):

    station_radius = 50
    station_height = 150

    color = '#fa7aa8'

    @staticmethod
    def build(canvas, shift):
        x0 = shift
        y0 = 150
        x1 = x0 + StationBuilder.station_radius
        y1 = y0 + StationBuilder.station_radius

        # canvas.bind("<Button-1>", partial(TrainBuilder.click, canvas))

        return canvas.create_oval(x0,y0 ,x1 ,y1, fill=StationBuilder.color)

    def build_text(canvas, shift, number):
        x0 = shift
        y0 = 150
        x1 = x0 + StationBuilder.station_radius
        y1 = y0 + StationBuilder.station_radius

        return canvas.create_text((x0 + x1) / 2 ,(y0 + y1) / 2, text=str(number))

    def build_label_r(canvas, shift, txt):
        y0 = 150
        x = shift + StationBuilder.station_radius / 2
        y = y0 + StationBuilder.station_radius + 100

        return canvas.create_text(x, y, text = txt)

    def build_label_l(canvas, shift, txt):
        y0 = 150
        x = shift + StationBuilder.station_radius / 2
        y = y0 - 100

        return canvas.create_text(x, y, text = txt)


class TrainBuilder(object):

    station_radius = 50
    above  = 30
    station_height = 150

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
    def build(canvas, station, direction, number):
        x0 = station.shift
        if (direction == 'r'):
            y0 = TrainBuilder.station_height + TrainBuilder.station_radius + TrainBuilder.above
        else:
            y0 = TrainBuilder.station_height - TrainBuilder.station_radius - TrainBuilder.above - TrainBuilder.height

        x1 = x0 + TrainBuilder.length
        y1 = y0 + TrainBuilder.height

        # canvas.bind("<Button-1>", partial(TrainBuilder.click, canvas))

        return canvas.create_oval(x0,y0 ,x1 ,y1, fill=COLORS[number*3])


    @staticmethod
    def build_text(canvas, station, direction, number):
        x0 = station.shift
        if (direction == 'r'):
            y0 = TrainBuilder.station_height + TrainBuilder.station_radius + TrainBuilder.above
        else:
            y0 = TrainBuilder.station_height - TrainBuilder.station_radius - TrainBuilder.above - TrainBuilder.height

        x1 = x0 + TrainBuilder.length
        y1 = y0 + TrainBuilder.height

        #so
        y = y1 + 10
        x = (x1 + x0) / 2

        return canvas.create_text(x, y, text=str(number))


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




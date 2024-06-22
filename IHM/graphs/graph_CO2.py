import pyqtgraph as pg
import numpy as np


class graph_co2(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='CO2 (ppm)', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.temp_plot = self.plot(pen=(29, 255, 84))
        self.temp_data = np.linspace(0, 0, 30)
        self.ptr = 0
    def update(self, value):
        self.temp_data[:-1] = self.temp_data[1:]
        self.temp_data[-1] = value
        self.ptr += 1
        self.temp_plot.setData(self.temp_data)
        self.temp_plot.setPos(self.ptr, 0)

    def updateForTime(self, value, time):
        self.temp_data[:-1] = self.temp_data[1:]
        self.temp_data[-1] = value
        self.ptr = time
        self.temp_plot.setData(self.temp_data)
        self.temp_plot.setPos(self.ptr, 0)

    def updateForAlt(self, value, altitude):
        self.temp_data[:-1] = self.temp_data[1:]
        self.temp_data[-1] = value
        self.ptr = altitude
        self.temp_plot.setData(self.temp_data)
        self.temp_plot.setPos(self.ptr, 0)
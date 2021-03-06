import sys
import matplotlib
from matplotlib import rcParams
matplotlib.use('Qt5agg')
rcParams.update({'figure.autolayout': True})

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.fig = fig

    def get_toolbar(self, plot):
        toolbar = NavigationToolbar(plot, self)
        toolbar.setStyleSheet("background-color:Gray;")
        return toolbar

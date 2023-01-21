from abc import ABC

import pandas as pd


class PlotterAbstract(ABC):
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, data: pd.DataFrame):
        self.data = data


class ActivityPlotterAbstract(PlotterAbstract):

    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

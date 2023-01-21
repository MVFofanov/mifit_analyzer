from abc import ABC
from pympler import asizeof

import pandas as pd


class PlotterAbstract(ABC):
    plots_directory = '/mnt/c/mifit_data/mifit_analyzer/plots'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def get_size(self) -> str:
        size_in_mb = asizeof.asizeof(self) / 1024 / 1024
        return f'{str(self).split("(")[0]} object size is {size_in_mb:.2f} Mb'


class ActivityPlotterAbstract(PlotterAbstract):

    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]


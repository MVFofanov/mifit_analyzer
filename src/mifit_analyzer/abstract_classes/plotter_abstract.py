from abc import ABC
from pympler import asizeof

import pandas as pd


class PlotterAbstract(ABC):
    # results_directory = '/mnt/c/mifit_data/mifit_analyzer/results'
    # plots_directory = f'{results_directory}/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, data: pd.DataFrame, results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results'):
        self.data = data

        self.results_directory = '/mnt/c/mifit_data/mifit_analyzer/results'
        self.plots_directory = f'{results_directory}/plots/'

    def get_size(self) -> str:
        size_in_mb = asizeof.asizeof(self) / 1024 / 1024
        return f'{str(self).split("(")[0]} object size is {size_in_mb:.2f} Mb'


class ActivityPlotterAbstract(PlotterAbstract):

    def __init__(self, data: pd.DataFrame, results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results'):
        super().__init__(data, results_directory)

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

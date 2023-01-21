from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from abstract_classes.plotter_abstract import ActivityPlotterAbstract


class ActivityStagePlotter(ActivityPlotterAbstract):

    def __init__(self, data: pd.DataFrame):

        super().__init__(data)

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]
        self.speed_km_h_axis_labels = [i for i in range(0, int(self.data.kilometers_per_hour.max()))]

    def make_activity_stage_histplot_km_h(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.histplot(self.data, x='kilometers_per_hour', bins=30)

        plt.xticks(self.speed_km_h_axis_labels)
        plt.title('Kilometers per hour plot', fontsize=self.title_fontsize)
        plt.xlabel("Kilometers per hour", fontsize=self.label_fontsize)
        plt.ylabel("Count", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_stage_histplot_km_h.png'))
        plt.close("all")

    def make_activity_stage_start_stop_hour_per_weekday_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="start_hour", y="stop_hour", hue="weekday_name")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Start and stop time plot', fontsize=self.title_fontsize)
        plt.xlabel("Start activity stage time", fontsize=self.label_fontsize)
        plt.ylabel("Stop activity stage time", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'activity_stage_start_stop_hour_per_weekday_scatterplot.png'))
        plt.close("all")

    def make_activity_stage_start_hour_and_steps_per_weekday_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="start_hour", y="steps", hue="weekday_name")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.steps_axis_labels)
        plt.title('Start activity stage time and steps plot', fontsize=self.title_fontsize)
        plt.xlabel("Start activity stage time", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'activity_stage_start_hour_and_steps_per_weekday_scatterplot.png'))
        plt.close("all")

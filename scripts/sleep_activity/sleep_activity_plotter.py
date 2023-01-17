from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class SleepActivityPlotter:
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, data: pd.DataFrame):

        self.data = data

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

    def make_sleep_activity_correlations_plot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        columns = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours',
                             'start_weekday_real', 'stop_weekday_real', 'start_month_real', 'year_real',
                             'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio',
                             'steps', 'distance', 'runDistance', 'calories']]

        correlations = columns.corr()
        correlations = correlations * 100
        sns.heatmap(correlations, annot=True, fmt='.0f')

        plt.title('Sleep activity correlations plot', fontsize=self.title_fontsize)
        plt.xlabel("Features", fontsize=self.label_fontsize)
        plt.ylabel("Features", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_activity_correlations_plot.png'))
        plt.close("all")

    def make_sleep_activity_steps_sleep_per_start_weekday_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="steps", y="totalSleepTime_hours", hue="start_weekday_name_real")

        plt.xticks(self.steps_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Steps and total sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Steps", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'sleep_activity_steps_sleep_per_start_weekday_scatterplot.png'))
        plt.close("all")

    def make_sleep_activity_steps_sleep_per_stop_weekday_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="steps", y="totalSleepTime_hours", hue="stop_weekday_name_real")

        plt.xticks(self.steps_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Steps and total sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Steps", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'sleep_activity_steps_sleep_per_stop_weekday_scatterplot.png'))
        plt.close("all")

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from activity import ActivityData
from base_mifit_data import convert_csv_to_markdown
from sleep import SleepData


class SleepActivityData(SleepData, ActivityData):
    statistics_file_name = './mifit_analyzer/statistics/sleep_activity_statistics'

    def __init__(self, sleep: SleepData, activity: ActivityData) -> None:

        self.sleep_for_merge: pd.DataFramee = \
            sleep.data[['date', 'deepSleepTime_hours',
                        'shallowSleepTime_hours', 'totalSleepTime_hours', 'start_weekday_real',
                        'stop_weekday_real', 'start_month_real', 'start_weekday_name_real',
                        'stop_weekday_name_real', 'start_month_name_real', 'stop_month_name_real',
                        'year_real', 'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio']]

        self.activity_for_merge: pd.DataFrame = activity.data[['date', 'steps', 'distance', 'runDistance', 'calories',
                                                               'date_month_name', 'date_weekday_name', 'year']]
        self.data: pd.DataFrame = pd.merge(self.sleep_for_merge, self.activity_for_merge, on='date')

        self.sleep_for_merge = None
        self.activity_for_merge = None

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

    def __repr__(self) -> str:
        return 'SleepActivityData()'

    def make_sleep_activity_correlations_plot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        correlations = self.data.corr()
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

    def write_statistics_to_csv(self) -> None:
        desired_columns = self.data.describe()[['totalSleepTime_hours', 'deepSleepTime_hours', 'shallowSleepTime_hours',
                                                'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio',
                                                'steps', 'distance', 'runDistance', 'calories']]\
            .round(2)

        desired_columns.columns = ['Total sleep time (hours)', 'Deep sleep time (hours)', 'Shallow sleep time (hours)',
                                   'Start sleep time', 'Stop sleep time', 'Deep sleep time/Total sleep time ratio',
                                   'Steps', 'Distance', 'Run distance', 'Calories']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)

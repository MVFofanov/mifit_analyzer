from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from mifit_data import MifitData


class Sleep(MifitData):
    directory_name = 'SLEEP'
    statistics_file_name = './mifit_analyzer/statistics/sleep_statistics'

    def __init__(self, start_date: str | None, end_date: str | None, hours_difference: int) -> None:
        self.data: pd.DataFrame = self.read_all_csv_files()

        self.date_min: datetime = self.data.date.min()
        self.date_max: datetime = self.data.date.max()

        if start_date is not None:
            self.start_date: datetime = datetime.strptime(start_date, '%Y.%m.%d')
        else:
            self.start_date = self.date_min

        if end_date is not None:
            self.end_date: datetime = datetime.strptime(end_date, '%Y.%m.%d')
        else:
            self.end_date = self.date_max

        self.hours_difference = hours_difference

    def __repr__(self) -> str:
        return f'Sleep(start_date={self.start_date}, end_date={self.end_date}, ' \
               f'hours_difference={self.hours_difference})'

    def select_date_range(self):
        if self.start_date != self.date_min or self.end_date != self.date_max:
            self.data = self.data[(self.data.date >= self.start_date) &
                                  (self.data.date <= self.end_date)]
            self.date_min: datetime = self.start_date
            self.date_max: datetime = self.end_date

    def transform_data_for_analysis(self) -> None:
        self.transform_time_columns_to_datetime()
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

    def transform_time_columns_to_datetime(self) -> None:
        self.data['date'] = pd.to_datetime(self.data['date'], unit='s')
        self.data['start'] = pd.to_datetime(self.data['start'], unit='s')
        self.data['stop'] = pd.to_datetime(self.data['stop'], unit='s')

    def add_new_columns(self) -> None:
        self.data['totalSleepTime'] = self.data.deepSleepTime + self.data.shallowSleepTime
        self.data['deepSleepTime_hours'] = round(self.data.deepSleepTime / 60, 2)
        self.data['shallowSleepTime_hours'] = round(self.data.shallowSleepTime / 60, 2)
        self.data['totalSleepTime_hours'] = round(self.data.totalSleepTime / 60, 2)
        self.data['start_real'] = self.data.start + timedelta(hours=self.hours_difference)
        self.data['stop_real'] = self.data.stop + timedelta(hours=self.hours_difference)
        self.data['start_weekday_real'] = self.data.start_real.dt.dayofweek
        self.data['stop_weekday_real'] = self.data.stop_real.dt.dayofweek
        self.data['start_month_real'] = self.data.start_real.dt.month
        self.data['start_weekday_name_real'] = self.data.start_real.dt.day_name()
        self.data['stop_weekday_name_real'] = self.data.stop_real.dt.day_name()
        self.data['start_month_name_real'] = self.data.start_real.dt.month_name()
        self.data['stop_month_name_real'] = self.data.stop_real.dt.month_name()
        self.data['year_real'] = self.data.start_real.dt.year
        self.data["start_weekday_name_real"] = self.data["start_weekday_name_real"].astype('category')
        self.data["start_weekday_name_real"] = self.data["start_weekday_name_real"].cat.set_categories(
            self.day_of_the_week_names)
        self.data["stop_weekday_name_real"] = self.data["stop_weekday_name_real"].astype('category')
        self.data["stop_weekday_name_real"] = self.data["stop_weekday_name_real"].cat.set_categories(
            self.day_of_the_week_names)
        self.data["start_month_name_real"] = self.data["start_month_name_real"].astype('category')
        self.data["start_month_name_real"] = self.data["start_month_name_real"].cat.set_categories(
            self.month_names)
        self.data["stop_month_name_real"] = self.data["stop_month_name_real"].astype('category')
        self.data["stop_month_name_real"] = self.data["stop_month_name_real"].cat.set_categories(
            self.month_names)
        self.data['start_time_real'] = round(self.data.start_real.dt.hour + self.data.start_real.dt.minute / 60, 2)
        self.data['stop_time_real'] = round(self.data.stop_real.dt.hour + self.data.stop_real.dt.minute / 60, 2)
        self.data['deep_total_sleep_ratio'] = self.data.deepSleepTime_hours / self.data.totalSleepTime_hours

    def make_sleep_hours_pairplot(self) -> None:
        sleep_hours = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']]

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.pairplot(sleep_hours)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_pairplot.png'))
        plt.close("all")

    def make_sleep_hours_boxplot(self) -> None:
        sleep_hours = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']]
        fig, axs = plt.subplots(ncols=3, nrows=1, figsize=self.plot_figsize)
        index = 0
        axs = axs.flatten()
        for k, v in sleep_hours.items():
            sns.boxplot(y=k, data=sleep_hours, ax=axs[index])
            index += 1
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)
        plt.close("all")

    def make_sleep_hours_correlations_plot(self) -> None:
        correlations = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']].corr()
        correlations = correlations * 100

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.heatmap(correlations, annot=True, fmt='.0f')

        plt.title('Sleep time correlations plot', fontsize=self.title_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_correlations_plot.png'))
        plt.close("all")

    def make_sleep_correlations_plot(self) -> None:
        correlations = self.data.corr()
        correlations = correlations * 100

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.heatmap(correlations, annot=True, fmt='.0f')

        plt.title('Sleep time correlations plot', fontsize=self.title_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_correlations_plot.png'))
        plt.close("all")

    def make_sleep_hours_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="shallowSleepTime_hours", y="deepSleepTime_hours",
                        hue="start_weekday_name_real")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow and deep sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Shallow sleep, hours", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep, hours", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_scatterplot.png'))
        plt.close("all")

    def make_sleep_hours_per_start_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per day of the week when fall asleep plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_per_start_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_stop_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="stop_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per day of the week when woke up plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_per_stop_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_start_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_per_start_month_boxplot.png'))
        plt.close("all")

    def make_sleep_start_and_stop_time_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="start_time_real", y="stop_time_real", hue="start_weekday_name_real")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Start and stop sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Start sleep time", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.path_to_plots, 'sleep_start_and_stop_time_scatterplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_start_time_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="stop_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_stop_time_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_start_time_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="stop_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_stop_time_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_start_time_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_stop_time_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_deep_hours_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_shallow_hours_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_deep_hours_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_shallow_hours_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_hours_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_deep_hours_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.path_to_plots, 'sleep_shallow_hours_per_year_boxplot.png'))
        plt.close("all")

    def write_statistics_to_csv(self) -> None:

        desired_columns = self.data.describe()[['totalSleepTime_hours', 'deepSleepTime_hours', 'shallowSleepTime_hours',
                                                'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio']]\
            .round(2)

        desired_columns.columns = ['Total sleep time (hours)', 'Deep sleep time (hours)', 'Shallow sleep time (hours)',
                                   'Start sleep time', 'Stop sleep time', 'Deep sleep time/Total sleep time ratio']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        self.convert_csv_to_markdown()

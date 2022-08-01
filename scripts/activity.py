from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from mifit_data import MifitData, convert_csv_to_markdown


class Activity(MifitData):
    directory_name = 'ACTIVITY'
    statistics_file_name = './mifit_analyzer/statistics/activity_statistics'

    def __init__(self, start_date: str | None, end_date: str | None, date_format: str) -> None:
        self.date_format = date_format

        self.data: pd.DataFrame = self.read_all_csv_files()

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

        self.date_min: datetime = self.data.date.min()
        self.date_max: datetime = self.data.date.max()

        if start_date is not None:
            self.start_date: datetime = datetime.strptime(start_date, self.date_format)
        else:
            self.start_date = self.date_min

        if end_date is not None:
            self.end_date: datetime = datetime.strptime(end_date, self.date_format)
        else:
            self.end_date = self.date_max

    def __repr__(self) -> str:
        return f'Activity(start_date={self.start_date}, end_date={self.end_date})'

    def transform_data_for_analysis(self) -> None:
        self.transform_time_columns_to_datetime()
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

    def transform_time_columns_to_datetime(self) -> None:
        self.data['date'] = pd.to_datetime(self.data['date'], unit='s')

    def add_new_columns(self) -> None:
        self.get_days_and_month_from_date()
        self.get_days_and_month_names()
        self.set_the_order_of_days_and_months()

    def get_days_and_month_from_date(self) -> None:
        self.data['date_weekday'] = self.data['date'].dt.dayofweek
        self.data['date_month'] = self.data['date'].dt.month
        self.data['year'] = self.data['date'].dt.year

    def get_days_and_month_names(self) -> None:
        self.data['date_weekday_name'] = self.data['date'].dt.day_name()
        self.data['date_month_name'] = self.data['date'].dt.month_name()

    def set_the_order_of_days_and_months(self) -> None:
        self.data['date_weekday_name'] = self.data['date_weekday_name'].astype('category')
        self.data['date_weekday_name'] = self.data['date_weekday_name'] \
            .cat.set_categories(self.day_of_the_week_names)
        self.data['date_month_name'] = self.data['date_month_name'].astype('category')
        self.data['date_month_name'] = self.data['date_month_name'] \
            .cat.set_categories(self.month_names)

    def make_activity_pairplot(self) -> None:
        activity_data = self.data[['steps', 'distance', 'runDistance', 'calories']]

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.pairplot(activity_data)

        plt.savefig(Path(self.plots_directory, 'activity_pairplot.png'))
        plt.close("all")

    def make_activity_boxplot(self) -> None:
        activity_data = self.data[['steps', 'distance', 'runDistance', 'calories']]
        fig, axs = plt.subplots(ncols=4, nrows=1, figsize=(10, 5))
        index = 0
        axs = axs.flatten()
        for k, v in activity_data.items():
            sns.boxplot(y=k, data=activity_data, ax=axs[index])
            index += 1
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)

        plt.savefig(Path(self.plots_directory, 'activity_boxplot.png'))
        plt.close("all")

    def make_activity_steps_distance_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="steps", y="distance", hue="date_weekday_name")

        plt.xticks(self.steps_axis_labels)
        plt.yticks(self.distance_axis_labels)
        plt.title('Steps and distance plot', fontsize=self.title_fontsize)
        plt.xlabel("Steps", fontsize=self.label_fontsize)
        plt.ylabel("Distance", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'activity_steps_distance_scatterplot.png'))
        plt.close("all")

    def make_activity_steps_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="date_weekday_name")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_weekday_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="date_weekday_name")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Distance", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_weekday_boxplot.png'))
        plt.close("all")

    def make_activity_steps_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="date_month_name")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_month_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="date_month_name")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Distance, m", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_month_boxplot.png'))
        plt.close("all")

    def make_activity_steps_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="year")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_year_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="year")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Distance, m", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_year_boxplot.png'))
        plt.close("all")

    def write_statistics_to_csv(self) -> None:
        desired_columns = self.data.describe()[['steps', 'distance', 'runDistance', 'calories']]\
            .round(2)

        desired_columns.columns = ['Steps', 'Distance', 'Run distance', 'Calories']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)

    def find_date_range_length_by_daily_steps_goal(self):
        pass

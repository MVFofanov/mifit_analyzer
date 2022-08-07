from datetime import datetime
import glob
from pathlib import Path
from typing import NamedTuple
import subprocess

import pandas as pd

from base_mifit_data import convert_csv_to_markdown
from sleep_activity import SleepActivityData


class TotalRecords(NamedTuple):
    start_date: str
    end_date: str
    available_days_percent: float
    daily_steps_goal_achieved_days_percent: float
    total_sleep_days_number: float
    total_sleep_days_percent: float
    total_distance_kilometers: float
    total_distance_kilosteps: float
    total_burned_kilocalories: float
    total_run_kilometers: float
    stride_length: float


class MifitReport:
    current_directory = './mifit_analyzer'
    plots_directory = './mifit_analyzer/plots'
    report_directory = './mifit_analyzer/report'
    statistics_directory = './mifit_analyzer/statistics'

    top_step_days_file_name = f'{statistics_directory}/top_step_days'

    def __init__(self, mifit_data: SleepActivityData, user_name: str, daily_steps_goal: int,
                 top_step_days_number: int, date_format: str) -> None:
        self.date_format = date_format

        self.mifit_data = mifit_data
        self.user = user_name
        self.daily_steps_goal = daily_steps_goal
        self.number_days = top_step_days_number

        self.markdown_plots_list: list[str] = []
        self.date_min: datetime = self.mifit_data.data.date.min()
        self.date_max: datetime = self.mifit_data.data.date.max()

        self.date_difference: int = (self.date_max - self.date_min).days + 1
        self.total_sleep_time_sum: int = self.mifit_data.data.totalSleepTime_hours.sum()
        self.distance_sum: int = self.mifit_data.data.distance.sum()
        self.steps_sum: int = self.mifit_data.data.steps.sum()
        self.daily_steps_goal_achieved_days: int = self.mifit_data.data[self.mifit_data.data.steps >=
                                                                        self.daily_steps_goal].shape[0]

        Path(self.report_directory).mkdir(parents=True, exist_ok=True)

    def __len__(self) -> int:
        return self.mifit_data.data.shape[0]

    def __repr__(self) -> str:
        return f'MifitReport(user_name={self.user}, daily_steps_goal={self.daily_steps_goal})'

    def make_report(self) -> None:
        today = datetime.now().strftime(self.date_format)

        markdown_list = [f'---\n'
                         f'title: "MiFit data analysis report"\n'
                         f'author: "{self.user}"\n'
                         f'date: {today}\n'
                         f'---']

        records = self.get_total_records()
        interesting_statistics = self.get_interesting_statistics(records)
        self.save_top_step_days()
        sleep_statistics, activity_statistics, top_step_days = self.get_mifit_statistics()

        markdown_list.extend((interesting_statistics,
                              'MiFit data sleep statistics\n', sleep_statistics,
                              'MiFit data activity statistics\n', activity_statistics,
                              f'MiFit data top {self.number_days} step days\n', top_step_days))

        markdown_list.extend(self.markdown_plots_list)

        self.save_report(markdown_list)
        self.convert_report_to_html()

    def get_all_plots_for_markdown_report(self) -> list[str]:
        all_png_files = glob.glob(f'{self.plots_directory}/*.png')
        plots_list = []
        for filename in all_png_files:
            plots_list.append(f"{filename.split('/')[-1]}")
            plots_list.append(f"![image]({filename})")
        return plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def save_report(self, markdown_list: list[str]) -> None:
        with open(f"{self.report_directory}/report.md", 'w') as file_md:
            file_md.write('\n'.join(markdown_list))

    def get_total_records(self):
        return TotalRecords(start_date=self.date_min.strftime(self.date_format),
                            end_date=self.date_max.strftime(self.date_format),
                            available_days_percent=round(len(self) / self.date_difference * 100, 2),
                            daily_steps_goal_achieved_days_percent=round(self.daily_steps_goal_achieved_days /
                                                                         len(self) * 100, 2),
                            total_sleep_days_number=round(self.total_sleep_time_sum / 24, 2),
                            total_sleep_days_percent=round(self.total_sleep_time_sum / 24 / len(self) * 100, 2),
                            total_distance_kilometers=round(self.distance_sum / 1000, 2),
                            total_distance_kilosteps=round(self.steps_sum / 1000, 2),
                            total_burned_kilocalories=round(self.mifit_data.data.calories.sum() / 1000, 2),
                            total_run_kilometers=round(self.mifit_data.data.runDistance.sum() / 1000, 2),
                            stride_length=round(self.distance_sum / self.steps_sum, 2)
                            )

    def get_interesting_statistics(self, records: TotalRecords) -> str:
        text = f'You have been wearing a fitness bracelet from {records.start_date} to ' \
               f'{records.end_date}.\n\n' \
               f'Data are available for {len(self)} ({records.available_days_percent}%) days out ' \
               f'of {self.date_difference} total days.\n\n' \
               f'Your daily steps goal is {self.daily_steps_goal} steps a day.\n\n' \
               f'You have successfully achieved your daily steps goal during {self.daily_steps_goal_achieved_days} ' \
               f'({records.daily_steps_goal_achieved_days_percent}%) days in total.\n\n' \
               f'You slept for {records.total_sleep_days_number} ' \
               f'({records.total_sleep_days_percent}%) days in total.\n\n' \
               f'You walked {records.total_distance_kilometers} kilometers in total.\n\n' \
               f'You walked {records.total_distance_kilosteps} thousand steps in total.\n\n' \
               f'You burned {records.total_burned_kilocalories} kilocalories while walking.\n\n' \
               f'You ran {records.total_run_kilometers} kilometers.\n\n' \
               f'Your stride length is ' \
               f'{records.stride_length} meter.\n\n'
        return text

    def get_mifit_statistics(self) -> tuple[str, str, str]:
        with open(f'{self.statistics_directory}/sleep_statistics.md') as file:
            sleep_statistics = file.read()

        with open(f'{self.statistics_directory}/activity_statistics.md') as file:
            activity_statistics = file.read()

        with open(f'{self.statistics_directory}/top_step_days.md') as file:
            top_step_days = file.read()

        return sleep_statistics, activity_statistics, top_step_days

    def save_top_step_days(self) -> None:
        top_step_days_df = self.mifit_data.data.sort_values(by='steps', ascending=False)[: self.number_days]

        columns = ['date', 'date_weekday_name', 'steps', 'distance', 'runDistance']
        top_step_days_df = top_step_days_df[columns]

        top_step_days_df['date'] = top_step_days_df['date'].apply(pd.to_datetime).dt.date

        top_step_days_df.columns = ['Date', 'Day', 'Steps', 'Distance', 'Run distance']

        top_step_days_df.to_csv(f'{self.statistics_directory}/top_step_days.csv', index=False)

        convert_csv_to_markdown(csv_file=self.top_step_days_file_name)

    def convert_report_to_html(self) -> None:
        arg_list = ['pandoc', '--self-contained', '-s', f'{self.report_directory}/report.md', '-o',
                    f'{self.report_directory}/report.html']
        stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out, err = stream.communicate()

    def make_sleep_plots(self) -> None:
        self._make_sleep_common_plots()
        self._make_sleep_hours_boxplots()
        self._make_sleep_deep_and_shallow_hours_boxplots()
        self._make_sleep_start_and_stop_time_plots()

    def _make_sleep_common_plots(self) -> None:
        self.mifit_data.make_sleep_hours_pairplot()
        self.mifit_data.make_sleep_hours_boxplot()
        self.mifit_data.make_sleep_hours_correlations_plot()
        self.mifit_data.make_sleep_correlations_plot()
        self.mifit_data.make_sleep_hours_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep common plots\n',
                                         *self.get_plot_markdown_text('sleep_hours_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_correlations_plot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_correlations_plot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_scatterplot'))

    def _make_sleep_start_and_stop_time_plots(self) -> None:
        self.mifit_data.make_sleep_start_and_stop_time_scatterplot()

        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_and_stop_time_scatterplot'))

        self._make_sleep_start_time_boxplots()
        self._make_sleep_stop_time_boxplots()

    def _make_sleep_start_time_boxplots(self) -> None:
        self.mifit_data.make_sleep_start_time_per_weekday_boxplot()
        self.mifit_data.make_sleep_start_time_per_month_boxplot()
        self.mifit_data.make_sleep_start_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep start time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_start_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_year_boxplot'))

    def _make_sleep_stop_time_boxplots(self) -> None:
        self.mifit_data.make_sleep_stop_time_per_weekday_boxplot()
        self.mifit_data.make_sleep_stop_time_per_month_boxplot()
        self.mifit_data.make_sleep_stop_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep stop time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_stop_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_hours_boxplots(self) -> None:
        self.mifit_data.make_sleep_hours_per_start_weekday_boxplot()
        self.mifit_data.make_sleep_hours_per_stop_weekday_boxplot()

        self.mifit_data.make_sleep_hours_per_start_month_boxplot()
        self.mifit_data.make_sleep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_hours_per_start_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_stop_weekday_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_start_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_deep_and_shallow_hours_boxplots(self) -> None:
        self._make_sleep_deep_hours_boxplots()
        self._make_sleep_shallow_hours_boxplots()

        self.markdown_plots_list.extend(('Here you can find your deep and shallow sleep hours_boxplots\n',
                                         *self.get_plot_markdown_text('sleep_deep_hours_boxplots')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_boxplots'))

    def _make_sleep_deep_hours_boxplots(self) -> None:
        self.mifit_data.make_sleep_deep_hours_per_weekday_boxplot()
        self.mifit_data.make_sleep_deep_hours_per_month_boxplot()
        self.mifit_data.make_sleep_deep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep deep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_deep_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_year_boxplot'))

    def _make_sleep_shallow_hours_boxplots(self) -> None:
        self.mifit_data.make_sleep_shallow_hours_per_weekday_boxplot()
        self.mifit_data.make_sleep_shallow_hours_per_month_boxplot()
        self.mifit_data.make_sleep_shallow_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep shallow hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_shallow_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_year_boxplot'))

    def make_activity_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your activity plots\n')

        self._make_activity_distance_common_plots()
        self._make_activity_distance_boxplots()
        self._make_activity_steps_boxplots()

    def _make_activity_distance_common_plots(self) -> None:
        self.mifit_data.make_activity_pairplot()
        self.mifit_data.make_activity_boxplot()
        self.mifit_data.make_activity_steps_distance_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your common activity plots\n',
                                         *self.get_plot_markdown_text('activity_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_distance_scatterplot'))

    def _make_activity_distance_boxplots(self) -> None:
        self.mifit_data.make_activity_distance_per_weekday_boxplot()
        self.mifit_data.make_activity_distance_per_month_boxplot()
        self.mifit_data.make_activity_distance_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity distance boxplots\n',
                                         *self.get_plot_markdown_text('activity_distance_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_year_boxplot'))

    def _make_activity_steps_boxplots(self) -> None:
        self.mifit_data.make_activity_steps_per_weekday_boxplot()
        self.mifit_data.make_activity_steps_per_month_boxplot()
        self.mifit_data.make_activity_steps_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity steps boxplots\n',
                                         *self.get_plot_markdown_text('activity_steps_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_year_boxplot'))

    def make_sleep_activity_plots(self) -> None:
        self.mifit_data.make_sleep_activity_correlations_plot()
        self.mifit_data.make_sleep_activity_steps_sleep_per_start_weekday_scatterplot()
        self.mifit_data.make_sleep_activity_steps_sleep_per_stop_weekday_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep activity plots\n',
                                         *self.get_plot_markdown_text('sleep_activity_correlations_plot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_start_weekday'
                                                                    '_scatterplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_stop_weekday'
                                                                    '_scatterplot'))

    def make_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your plots\n')

        self.make_sleep_plots()
        self.make_activity_plots()
        self.make_sleep_activity_plots()

    def make_statistics(self) -> None:
        pass

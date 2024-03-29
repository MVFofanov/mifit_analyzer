from dataclasses import dataclass
from datetime import datetime
import glob
import logging
from pathlib import Path
from pympler import asizeof
import subprocess

import pandas as pd

from abstract_classes import convert_csv_to_markdown, markdown_text
from activity import ActivityData, ActivityPlotter, ActivityReportPlotter
from activity_stage import ActivityStageData, ActivityStagePlotter, ActivityStageReportPlotter
from mifit_dataclasses import MiFitData
from sleep import SleepData, SleepPlotter, SleepReportPlotter
from sleep_activity import SleepActivityData, SleepActivityPlotter, SleepActivityReportPlotter


@dataclass(slots=True, frozen=True)
class TotalRecords:
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

    def __init__(self, mifit_data: MiFitData,
                 user_name: str, daily_steps_goal: int,
                 top_step_days_number: int, date_format: str,
                 results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results') -> None:
        self.results_directory = results_directory
        self.plots_directory = f'{results_directory}/plots/'
        self.statistics_directory = f'{results_directory}/statistics'
        self.report_directory = f'{results_directory}/report'
        self.top_step_days_file_name = f'{self.statistics_directory}/top_step_days'

        self.date_format = date_format

        self.mifit_data: MiFitData = mifit_data
        self.sleep: SleepData = mifit_data.sleep
        self.activity: ActivityData = mifit_data.activity
        self.sleep_activity: SleepActivityData = mifit_data.sleep_activity
        self.activity_stage: ActivityStageData = mifit_data.activity_stage

        self.user = user_name
        self.daily_steps_goal = daily_steps_goal
        self.number_days = top_step_days_number

        self.markdown_plots_list: list[markdown_text] = []
        self.date_min: datetime = self.activity.data.date.min()
        self.date_max: datetime = self.activity.data.date.max()

        self.date_difference: int = (self.date_max - self.date_min).days + 1
        self.total_sleep_time_sum: int = self.sleep.data.totalSleepTime_hours.sum()
        self.distance_sum: int = self.activity.data.distance.sum()
        self.steps_sum: int = self.activity.data.steps.sum()
        self.daily_steps_goal_achieved_days: int = self.activity.data[self.activity.data.steps >=
                                                                      self.daily_steps_goal].shape[0]

        Path(self.report_directory).mkdir(parents=True, exist_ok=True)

    def __len__(self) -> int:
        return self.activity.data.shape[0]

    def __repr__(self) -> str:
        cls_name = type(self).__name__

        return f"{cls_name}(mifit_data={type(self.mifit_data).__name__}, "\
               f"user_name='{self.user}', daily_steps_goal={self.daily_steps_goal}, "\
               f"top_step_days_number={self.number_days}, "\
               f"date_format='{self.date_format}', "\
               f"results_directory='{self.results_directory}')"

    def make_logging_message(self):
        logging.info(f"{self}")
        logging.info(f"{self.get_size()}")

    def make_report(self) -> None:
        today = datetime.now().strftime(self.date_format)

        markdown_list = [f'---\n'
                         f'title: "MiFit data analysis report"\n'
                         f'author: "{self.user}"\n'
                         f'date: {today}\n'
                         f'---']

        records = self.get_total_records()

        logging.info('Records have been calculated')

        interesting_statistics = self.get_interesting_statistics(records)

        logging.info('Interesting_statistics have been calculated')

        self.save_top_step_days()
        sleep_statistics, activity_statistics, activity_stage_statistics, top_step_days = self.get_mifit_statistics()

        markdown_list.extend((interesting_statistics,
                              'MiFit data sleep statistics\n', sleep_statistics,
                              'MiFit data activity statistics\n', activity_statistics,
                              'MiFit data activity stage statistics\n', activity_stage_statistics,
                              f'MiFit data top {self.number_days} step days\n', top_step_days))

        markdown_list.extend(self.markdown_plots_list)

        self.save_report(markdown_list)

        logging.info('Report has been saved as .md file')

        self.convert_report_to_html()

        logging.info('Report has been saved as .html file')

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

    def get_total_records(self) -> TotalRecords:
        return TotalRecords(start_date=self.date_min.strftime(self.date_format),
                            end_date=self.date_max.strftime(self.date_format),
                            available_days_percent=round(len(self) / self.date_difference * 100, 2),
                            daily_steps_goal_achieved_days_percent=round(self.daily_steps_goal_achieved_days /
                                                                         len(self) * 100, 2),
                            total_sleep_days_number=round(self.total_sleep_time_sum / 24, 2),
                            total_sleep_days_percent=round(self.total_sleep_time_sum / 24 / len(self) * 100, 2),
                            total_distance_kilometers=round(self.distance_sum / 1000, 2),
                            total_distance_kilosteps=round(self.steps_sum / 1000, 2),
                            total_burned_kilocalories=round(self.activity.data.calories.sum() / 1000, 2),
                            total_run_kilometers=round(self.activity.data.runDistance.sum() / 1000, 2),
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

    def get_mifit_statistics(self) -> tuple[str, ...]:
        with open(f'{self.statistics_directory}/sleep_statistics.md') as file:
            sleep_statistics = file.read()

        with open(f'{self.statistics_directory}/activity_statistics.md') as file:
            activity_statistics = file.read()

        with open(f'{self.statistics_directory}/activity_stage_statistics.md') as file:
            activity_stage_statistics = file.read()

        with open(f'{self.statistics_directory}/top_step_days.md') as file:
            top_step_days = file.read()

        return sleep_statistics, activity_statistics, activity_stage_statistics, top_step_days

    def save_top_step_days(self) -> None:
        top_step_days_df = self.activity.data.sort_values(by='steps', ascending=False)[: self.number_days]

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

    def make_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your plots\n')

        sleep_plotter = SleepPlotter(self.sleep.data, results_directory=self.results_directory)

        sleep_plotter.make_logging_message()

        sleep_report_plotter = SleepReportPlotter(plotter=sleep_plotter,
                                                  markdown_plots_list=self.markdown_plots_list)

        sleep_report_plotter.make_logging_message()

        sleep_report_plotter.make_plots()

        logging.info('Sleep plots have been successfully built')

        activity_plotter = ActivityPlotter(self.activity.data, results_directory=self.results_directory)

        activity_plotter.make_logging_message()

        activity_report_plotter = ActivityReportPlotter(plotter=activity_plotter,
                                                        markdown_plots_list=self.markdown_plots_list)

        activity_report_plotter.make_logging_message()

        activity_report_plotter.make_plots()

        logging.info('Activity plots have been successfully built')

        sleep_activity_plotter = SleepActivityPlotter(self.sleep_activity.data,
                                                      results_directory=self.results_directory)

        sleep_activity_plotter.make_logging_message()

        sleep_activity_report_plotter = SleepActivityReportPlotter(plotter=sleep_activity_plotter,
                                                                   markdown_plots_list=self.markdown_plots_list)

        sleep_activity_report_plotter.make_logging_message()

        sleep_activity_report_plotter.make_plots()

        logging.info('Sleep_activity plots have been successfully built')

        activity_stage_plotter = ActivityStagePlotter(self.activity_stage.data,
                                                      results_directory=self.results_directory)

        activity_stage_plotter.make_logging_message()

        activity_stage_report_plotter = ActivityStageReportPlotter(plotter=activity_stage_plotter,
                                                                   markdown_plots_list=self.markdown_plots_list)

        activity_stage_report_plotter.make_logging_message()

        activity_stage_report_plotter.make_plots()

        logging.info('Activity_stage plots have been successfully built')

    def make_statistics(self) -> None:
        pass

    def get_size(self) -> str:
        size_in_mb = asizeof.asizeof(self) / 1024 / 1024
        return f'{str(self).split("(")[0]} object size is {size_in_mb:.2f} Mb'

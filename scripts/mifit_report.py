from datetime import datetime
import glob
import subprocess

from sleep_activity import SleepActivity


class MifitReport:
    current_dir = './mifit_analyzer'
    plots_dir = './mifit_analyzer/plots'

    def __init__(self, mifit_data: SleepActivity, user_name: str, daily_steps_goal: int):
        self.mifit_data = mifit_data
        self.user = user_name
        self.daily_steps_goal = daily_steps_goal

        self.markdown_plots_list = []
        self.date_min: datetime = self.mifit_data.data.date.min()
        self.date_max: datetime = self.mifit_data.data.date.max()

        self.date_difference: int = (self.date_max - self.date_min).days + 1
        self.total_sleep_time_sum: int = self.mifit_data.data.totalSleepTime_hours.sum()
        self.distance_sum: int = self.mifit_data.data.distance.sum()
        self.steps_sum: int = self.mifit_data.data.steps.sum()
        self.daily_steps_goal_achieved_days: int = self.mifit_data.data[self.mifit_data.data.steps >=
                                                                        self.daily_steps_goal].shape[0]

    def __len__(self) -> int:
        return self.mifit_data.data.shape[0]

    def __repr__(self) -> str:
        return repr(self.mifit_data.data.describe())

    def make_report(self) -> None:
        today = datetime.now().strftime('%Y.%m.%d')

        markdown_list = [f'---\n'
                         f'title: "MiFit data analysis report"\n'
                         f'author: "{self.user}"\n'
                         f'date: {today}\n'
                         f'---']

        interesting_statistics = self.get_interesting_statistics()
        sleep_statistics, activity_statistics = self.get_mifit_statistics()

        self.save_top_step_days_to_csv()

        markdown_list.extend((interesting_statistics,
                              'MiFit data sleep statistics\n', sleep_statistics,
                              'MiFit data activity statistics\n', activity_statistics))

        # markdown_list.extend(self.get_all_plots_for_markdown_report())
        markdown_list.extend(self.markdown_plots_list)

        self.save_report(markdown_list)
        self.convert_markdown_to_html()

    def get_all_plots_for_markdown_report(self) -> list[str]:
        all_png_files = glob.glob(f'{self.current_dir}/plots/*.png')
        plots_list = []
        for filename in all_png_files:
            plots_list.append(f"{filename.split('/')[-1]}")
            plots_list.append(f"![image]({filename})")
        return plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.current_dir}/plots/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def save_report(self, markdown_list: list[str]) -> None:
        with open(f"{self.current_dir}/report/report.md", 'w') as file_md:
            file_md.write('\n'.join(markdown_list))

    def get_interesting_statistics(self) -> str:
        text = f'You have been wearing a fitness bracelet from {self.date_min.strftime("%Y.%m.%d")} to ' \
               f'{self.date_max.strftime("%Y.%m.%d")}.\n\n' \
               f'Data are available for {len(self)} ({round(len(self) / self.date_difference * 100, 2)}%) days out ' \
               f'of {self.date_difference} total days.\n\n' \
               f'Your daily steps goal is {self.daily_steps_goal} steps a day.\n\n' \
               f'You have successfully achieved your daily steps goal during {self.daily_steps_goal_achieved_days} ' \
               f'({round(self.daily_steps_goal_achieved_days / len(self) * 100, 2)}%) days in total.\n\n' \
               f'You slept for {round(self.total_sleep_time_sum / 24, 2)} ' \
               f'({round(self.total_sleep_time_sum / 24 / len(self) * 100, 2)}%) days in total.\n\n' \
               f'You walked {round(self.distance_sum / 1000, 2)} kilometers in total.\n\n' \
               f'You walked {round(self.steps_sum / 1000, 2)} thousand steps in total.\n\n' \
               f'You burned {round(self.mifit_data.data.calories.sum() / 1000, 2)} kilocalories while walking.\n\n' \
               f'You ran {round(self.mifit_data.data.runDistance.sum() / 1000, 2)} kilometers.\n\n' \
               f'Your stride length is ' \
               f'{round(self.distance_sum / self.steps_sum, 2)} meter.\n\n'
        return text

    def get_mifit_statistics(self) -> tuple[str, str]:
        with open('./mifit_analyzer/statistics/sleep_statistics.md') as file:
            sleep_statistics = file.read()

        with open('./mifit_analyzer/statistics/activity_statistics.md') as file:
            activity_statistics = file.read()

        return sleep_statistics, activity_statistics

    def save_top_step_days_to_csv(self, number_days=10):
        top_step_days_df = self.mifit_data.data.sort_values(by='steps', ascending=False)[: number_days]

        # top_step_days_df = self.mifit_data.data[: number_days]

        columns = ['date', 'steps', 'distance', 'runDistance', 'calories',
                   'date_month_name', 'date_weekday_name', 'year']

        top_step_days_df[columns].to_csv(f'{self.current_dir}/statistics/top_step_days.csv')

    def convert_markdown_to_html(self) -> None:
        arg_list = ['pandoc', '--self-contained', '-s', './mifit_analyzer/report/report.md', '-o',
                    './mifit_analyzer/report/report.html']
        stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out, err = stream.communicate()

    def convert_csv_to_markdown(self) -> None:
        arg_list = ['pandoc', '-f', 'csv', '-t', 'markdown',
                    '-s', f'{self.statistics_file_name}.csv',
                    '-o', f'{self.statistics_file_name}.md']
        stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out, err = stream.communicate()

    def make_sleep_plots(self):
        self._make_sleep_common_plots()
        self._make_sleep_hours_boxplots()
        self._make_sleep_deep_and_shallow_hours_boxplots()
        self._make_sleep_start_and_stop_time_plots()

    def _make_sleep_common_plots(self):
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

    def _make_sleep_start_and_stop_time_plots(self):
        self.mifit_data.make_sleep_start_and_stop_time_scatterplot()

        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_and_stop_time_scatterplot'))

        self._make_sleep_start_time_boxplots()
        self._make_sleep_stop_time_boxplots()

    def _make_sleep_start_time_boxplots(self):
        self.mifit_data.make_sleep_start_time_per_weekday_boxplot()
        self.mifit_data.make_sleep_start_time_per_month_boxplot()
        self.mifit_data.make_sleep_start_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep start time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_start_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_year_boxplot'))

    def _make_sleep_stop_time_boxplots(self):
        self.mifit_data.make_sleep_stop_time_per_weekday_boxplot()
        self.mifit_data.make_sleep_stop_time_per_month_boxplot()
        self.mifit_data.make_sleep_stop_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep stop time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_stop_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_hours_boxplots(self):
        self.mifit_data.make_sleep_hours_per_start_weekday_boxplot()
        self.mifit_data.make_sleep_hours_per_stop_weekday_boxplot()

        self.mifit_data.make_sleep_hours_per_start_month_boxplot()
        self.mifit_data.make_sleep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_hours_per_start_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_stop_weekday_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_start_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_deep_and_shallow_hours_boxplots(self):
        self._make_sleep_deep_hours_boxplots()
        self._make_sleep_shallow_hours_boxplots()

        self.markdown_plots_list.extend(('Here you can find your deep and shallow sleep hours_boxplots\n',
                                         *self.get_plot_markdown_text('sleep_deep_hours_boxplots')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_boxplots'))

    def _make_sleep_deep_hours_boxplots(self):
        self.mifit_data.make_sleep_deep_hours_per_weekday_boxplot()
        self.mifit_data.make_sleep_deep_hours_per_month_boxplot()
        self.mifit_data.make_sleep_deep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep deep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_deep_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_year_boxplot'))

    def _make_sleep_shallow_hours_boxplots(self):
        self.mifit_data.make_sleep_shallow_hours_per_weekday_boxplot()
        self.mifit_data.make_sleep_shallow_hours_per_month_boxplot()
        self.mifit_data.make_sleep_shallow_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep shallow hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_shallow_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_year_boxplot'))

    def make_activity_plots(self):
        self.markdown_plots_list.append('Here you can find your activity plots\n')

        self._make_activity_distance_common_plots()
        self._make_activity_distance_boxplots()
        self._make_activity_steps_boxplots()

    def _make_activity_distance_common_plots(self):
        self.mifit_data.make_activity_pairplot()
        self.mifit_data.make_activity_boxplot()
        self.mifit_data.make_activity_steps_distance_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your common activity plots\n',
                                         *self.get_plot_markdown_text('activity_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_distance_scatterplot'))

    def _make_activity_distance_boxplots(self):
        self.mifit_data.make_activity_distance_per_weekday_boxplot()
        self.mifit_data.make_activity_distance_per_month_boxplot()
        self.mifit_data.make_activity_distance_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity distance boxplots\n',
                                         *self.get_plot_markdown_text('activity_distance_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_year_boxplot'))

    def _make_activity_steps_boxplots(self):
        self.mifit_data.make_activity_steps_per_weekday_boxplot()
        self.mifit_data.make_activity_steps_per_month_boxplot()
        self.mifit_data.make_activity_steps_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity steps boxplots\n',
                                         *self.get_plot_markdown_text('activity_steps_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_year_boxplot'))

    def make_sleep_activity_plots(self):
        self.mifit_data.make_sleep_activity_correlations_plot()
        self.mifit_data.make_sleep_activity_steps_sleep_per_start_weekday_scatterplot()
        self.mifit_data.make_sleep_activity_steps_sleep_per_stop_weekday_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep activity plots\n',
                                         *self.get_plot_markdown_text('sleep_activity_correlations_plot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_start_weekday'
                                                                    '_scatterplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_stop_weekday'
                                                                    '_scatterplot'))

    def make_plots(self):
        self.markdown_plots_list.append('Here you can find your plots\n')

        self.make_sleep_plots()
        self.make_activity_plots()
        self.make_sleep_activity_plots()

    def make_statistics(self):
        pass

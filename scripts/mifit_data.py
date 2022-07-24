from datetime import datetime
import glob
from pathlib import Path
import subprocess

import pandas as pd


class MifitData:
    plot_figsize = (12, 8)
    path_to_plots = './mifit_analyzer/plots/'
    statistics_directory = './mifit_analyzer/statistics/'

    day_of_the_week_names = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    month_names = ('January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December')

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16

    def __init__(self) -> None:
        self.data = None
        self.directory_name: str | None = None
        self.user = None
        self.statistics_file_name = None

    def __len__(self) -> int:
        return self.data.shape[0]

    def __repr__(self) -> str:
        return repr(self.data.describe())

    def transform_data_for_analysis(self) -> None:
        raise NotImplementedError

    def write_statistics_to_csv(self) -> None:
        raise NotImplementedError

    def transform_time_columns_to_datetime(self) -> None:
        self.data['date'] = self.data['date'].apply(pd.to_datetime)

    def add_new_columns(self) -> None:
        raise NotImplementedError

    def read_all_csv_files(self) -> pd.DataFrame:
        current_dir = str(Path().resolve())
        all_csv_files = glob.glob(f'{current_dir}/{self.directory_name}/*.csv')
        df_list = []

        for filename in all_csv_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            df_list.append(df)

        df = pd.concat(df_list, axis=0, ignore_index=True)
        return df

    def read_my_csv_file(self, path) -> None:
        self.data = pd.read_csv(path, index_col=None, header=0)

    def create_service_directories(self):
        Path(self.statistics_directory).mkdir(parents=True, exist_ok=True)
        Path(self.path_to_plots).mkdir(parents=True, exist_ok=True)

    def make_report(self) -> None:
        current_dir = './mifit_analyzer'
        all_png_files = glob.glob(f'{current_dir}/plots/*.png')
        today = datetime.now().strftime('%Y-%m-%d')

        with open('./mifit_analyzer/statistics/sleep_statistics.md') as file:
            sleep_statistics = file.read()

        with open('./mifit_analyzer/statistics/activity_statistics.md') as file:
            activity_statistics = file.read()

        markdown_list = [f'---\ntitle: "MiFit data analysis report"\nauthor: "{self.user}"\ndate: {today}\n---'
                         ]

        interesting_statistics = f'You have been wearing a fitness bracelet for {len(self)} days' \
                                 f'Dates: {self.data.date.min()}-{self.data.date.max()}.\n\n' \
                                 f'You slept for {round(self.data.totalSleepTime_hours.sum() / 24, 2)} \
                                 ({round(self.data.totalSleepTime_hours.sum() / 24 / len(self) * 100, 2)}%)' \
                                 ' days in total.\n\n' \
                                 f'You walked {round(self.data.distance.sum() / 1000, 2)} kilometers in total.\n\n' \
                                 f'You walked {self.data.steps.sum() / 1000} thousand steps in total.\n\n' \
                                 f'You burned {self.data.calories.sum() / 1000} kilocalories while walking.\n\n' \
                                 f'You ran {round(self.data.runDistance.sum() / 1000, 2)} kilometers.\n\n' \
                                 f'Your stride length is {round(self.data.distance.sum() / self.data.steps.sum(), 2)}' \
                                 ' meter.\n\n'

        markdown_list.extend((interesting_statistics,
                              'MiFit data sleep statistics\n', sleep_statistics,
                              'MiFit data activity statistics\n', activity_statistics))

        for filename in all_png_files:
            markdown_list.append(f"{filename.split('/')[-1].capitalize()}")
            markdown_list.append(f"![image]({filename})")

        with open(f"{current_dir}/report/report.md", 'w') as file_md:
            file_md.write('\n'.join(markdown_list))

        self.convert_markdown_to_html()

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

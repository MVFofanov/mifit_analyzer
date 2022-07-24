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
        return 'MifitData()'

    def transform_data_for_analysis(self) -> None:
        raise NotImplementedError

    def write_statistics_to_csv(self) -> None:
        raise NotImplementedError

    def transform_time_columns_to_datetime(self) -> None:
        raise NotImplementedError

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

    @staticmethod
    def convert_markdown_to_html() -> None:
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

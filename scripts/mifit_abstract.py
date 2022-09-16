from abc import ABC, abstractmethod
import glob
from datetime import datetime
from pathlib import Path
import subprocess

import pandas as pd


def convert_csv_to_markdown(csv_file: str) -> None:
    arg_list = ['pandoc', '-f', 'csv', '-t', 'markdown',
                '-s', f'{csv_file}.csv',
                '-o', f'{csv_file}.md']
    stream = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    out, err = stream.communicate()


def read_my_csv_file(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, index_col=None, header=0)
    return data


class MiFitDataAbstract(ABC):
    current_directory = './mifit_analyzer'
    plots_directory = './mifit_analyzer/plots/'
    statistics_directory = './mifit_analyzer/statistics/'

    day_of_the_week_names = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    month_names = ('January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December')

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self) -> None:
        self.directory_name: str | None = None
        self.statistics_file_name: str | None = None

        self.data = pd.DataFrame(columns=['A', 'B', 'C'], index=range(3))

        self.start_date = self.end_date = self.date_min = self.date_max = datetime.now()

    def __len__(self) -> int:
        return self.data.shape[0]

    def __repr__(self) -> str:
        return 'BaseMifitData()'

    @abstractmethod
    def transform_data_for_analysis(self) -> None:
        pass

    @abstractmethod
    def transform_time_columns_to_datetime(self) -> None:
        pass

    @abstractmethod
    def add_new_columns(self) -> None:
        pass

    @abstractmethod
    def write_statistics_to_csv(self) -> None:
        pass

    def read_all_csv_files(self) -> pd.DataFrame:
        current_dir = str(Path().resolve())
        all_csv_files = glob.glob(f'{current_dir}/{self.directory_name}/*.csv')
        df_list = []

        for filename in all_csv_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            df_list.append(df)

        df = pd.concat(df_list, axis=0, ignore_index=True)
        return df

    def create_service_directories(self) -> None:
        Path(self.statistics_directory).mkdir(parents=True, exist_ok=True)
        Path(self.plots_directory).mkdir(parents=True, exist_ok=True)

    def select_date_range(self) -> None:
        if self.start_date != self.date_min or self.end_date != self.date_max:
            self.data = self.data[(self.data.date >= self.start_date) &
                                  (self.data.date <= self.end_date)]

    # def print_size_of_object(self, obj) -> None:
    #     return print(f'{str(obj).split("(")[0]} object size is {round(asizeof.asizeof(obj) / 1024 / 1024, 2)} Mb')

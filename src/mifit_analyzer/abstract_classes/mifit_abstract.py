from abc import ABC, abstractmethod
import glob
from datetime import datetime
from pathlib import Path
from pympler import asizeof
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
    current_directory = '/mnt/c/mifit_data/mifit_analyzer'
    # results_directory = '/mnt/c/mifit_data/mifit_analyzer/results'
    # plots_directory = f'{results_directory}/plots/'
    # statistics_directory = f'{results_directory}/statistics/'

    day_of_the_week_names = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    month_names = ('January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December')

    def __init__(self, input_directory: str = '/mnt/c/mifit_data/mifit_analyzer/data',
                 start_date: str | None = None, end_date: str | None = None,
                 date_format: str = '%Y.%m.%d',
                 results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results',
                 hours_difference: int = 0
                 ) -> None:
        self.input_directory = input_directory.removesuffix('/')
        self.results_directory = results_directory.removesuffix('/')
        self.plots_directory = f'{results_directory}/plots/'
        self.statistics_directory = f'{results_directory}/statistics'
        #self.input_directory = f'{self.input_directory}/DATA_DIRECTORY_ABSTRACT'

        # self.input_directory = self.input_directory.removesuffix('/')
        self.statistics_file_name = f'{self.statistics_directory}/abstract_statistics'

        self.start_date = start_date
        self.end_date = end_date
        self.hours_difference = hours_difference
        self.date_format = date_format

        self.data: pd.DataFrame = self.read_all_csv_files()

        self.transform_time_columns_to_datetime()

        self.date_min: datetime = self.data.date.min()
        self.date_max: datetime = self.data.date.max()

        self.set_start_date_and_end_date()

        self.is_prepared = False

    def __len__(self) -> int:
        return self.data.shape[0]

    def __repr__(self) -> str:
        return 'BaseMifitData()'

    def set_start_date_and_end_date(self):
        if self.start_date is None:
            self.start_date = self.date_min
        else:
            self.start_date: datetime = datetime.strptime(self.start_date, self.date_format)

        if self.end_date is None:
            self.end_date = self.date_max
        else:
            self.end_date: datetime = datetime.strptime(self.end_date, self.date_format)

    @abstractmethod
    def transform_data_for_analysis(self) -> None:
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

        self.is_prepared = True

    @abstractmethod
    def transform_time_columns_to_datetime(self) -> None:
        self.data['date'] = pd.to_datetime(self.data['date'], unit='s')

    @abstractmethod
    def write_statistics_to_csv(self) -> None:
        pass

    def read_all_csv_files(self) -> pd.DataFrame:
        all_csv_files = glob.glob(f'{self.input_directory}/*.csv')
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

    def get_size(self) -> str:
        size_in_mb = asizeof.asizeof(self) / 1024 / 1024
        return f'{str(self).split("(")[0]} object size is {size_in_mb:.2f} Mb'

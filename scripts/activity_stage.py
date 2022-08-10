from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from base_mifit_data import BaseMifitData, convert_csv_to_markdown


class ActivityStageData(BaseMifitData):
    directory_name = 'ACTIVITY_STAGE'
    statistics_file_name = './mifit_analyzer/statistics/activity_stage_statistics'

    def __init__(self, start_date: str | None, end_date: str | None, date_format: str) -> None:
        self.date_format = date_format

        self.data: pd.DataFrame = self.read_all_csv_files()

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
        return f'ActivityData(start_date={self.start_date}, end_date={self.end_date})'

    def transform_data_for_analysis(self) -> None:
        self.transform_time_columns_to_datetime()
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

    def transform_time_columns_to_datetime(self) -> None:
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['start'] = pd.to_datetime(self.data['start'])
        self.data['stop'] = pd.to_datetime(self.data['stop'])

    def add_new_columns(self):
        self.data['minute_difference'] = (self.data.stop - self.data.start) / pd.Timedelta(minutes=1)
        self.data['steps_per_minute'] = self.data.steps / self.data.minute_difference
        self.data['meters_per_minute'] = self.data.distance / self.data.minute_difference
        self.data['meters_per_second'] = self.data.meters_per_minute / 60
        self.data['kilometers_per_hour'] = self.data.meters_per_second * 3600 / 1000

    def write_statistics_to_csv(self) -> None:

        desired_columns = self.data.describe()[['distance', 'calories', 'steps',
                                                'minute_difference', 'steps_per_minute', 'meters_per_minute',
                                                'meters_per_second', 'kilometers_per_hour']]\
            .round(2)

        desired_columns.columns = ['Distance, (meters)', 'Calories', 'Steps',
                                   'Stage duration, (minutes)', 'Steps/min', 'm/min',
                                   'm/s', 'km/h']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)
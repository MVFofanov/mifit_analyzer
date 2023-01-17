from datetime import datetime

import pandas as pd

from abstract_classes.mifit_abstract import MiFitDataAbstract, convert_csv_to_markdown


class ActivityData(MiFitDataAbstract):
    directory_name = 'ACTIVITY'
    statistics_file_name = './mifit_analyzer/statistics/activity_statistics'

    def __init__(self, start_date: str | None, end_date: str | None, date_format: str) -> None:
        self.date_format = date_format

        self.is_prepared = False

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

        self.is_prepared = True

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

    def write_statistics_to_csv(self) -> None:
        desired_columns = self.data.describe()[['steps', 'distance', 'runDistance', 'calories']]\
            .round(2)

        desired_columns.columns = ['Steps', 'Distance', 'Run distance', 'Calories']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)

    def find_date_range_length_by_daily_steps_goal(self):
        pass

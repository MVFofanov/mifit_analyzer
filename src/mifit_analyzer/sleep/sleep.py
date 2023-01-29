from datetime import timedelta

import pandas as pd

from abstract_classes.mifit_abstract import MiFitDataAbstract, convert_csv_to_markdown


class SleepData(MiFitDataAbstract):

    def __init__(self, input_directory: str = '/mnt/c/mifit_data/mifit_analyzer/data/SLEEP',
                 start_date: str | None = None, end_date: str | None = None,
                 date_format: str = '%Y.%m.%d',
                 results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results',
                 hours_difference: int = 0) -> None:

        super().__init__(input_directory, start_date, end_date, date_format, results_directory,
                         hours_difference)
        self.statistics_file_name = f'{self.statistics_directory}/sleep_statistics'

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        start_date = self.start_date.strftime(self.date_format)
        end_date = self.end_date.strftime(self.date_format)
        return f"{cls_name}(input_directory='{self.input_directory}', "\
               f"start_date='{start_date}', end_date='{end_date}', "\
               f"date_format='{self.date_format}', "\
               f"results_directory='{self.results_directory}', "\
               f"hours_difference={self.hours_difference})"

    def transform_data_for_analysis(self) -> None:
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

        self.is_prepared = True

    def transform_time_columns_to_datetime(self) -> None:
        super().transform_time_columns_to_datetime()
        self.data['start'] = pd.to_datetime(self.data['start'], unit='s')
        self.data['stop'] = pd.to_datetime(self.data['stop'], unit='s')

    def add_new_columns(self) -> None:
        self.data['totalSleepTime'] = self.data.deepSleepTime + self.data.shallowSleepTime
        self.convert_sleep_minutes_to_hours()
        self.get_real_start_and_stop_time()
        self.get_days_and_month_from_date()
        self.get_days_and_month_names()
        self.set_the_order_of_days_and_months()
        self.data['deep_total_sleep_ratio'] = self.data.deepSleepTime_hours / self.data.totalSleepTime_hours

    def convert_sleep_minutes_to_hours(self) -> None:
        self.data['deepSleepTime_hours'] = round(self.data.deepSleepTime / 60, 2)
        self.data['shallowSleepTime_hours'] = round(self.data.shallowSleepTime / 60, 2)
        self.data['totalSleepTime_hours'] = round(self.data.totalSleepTime / 60, 2)

    def get_real_start_and_stop_time(self) -> None:
        self.data['start_real'] = self.data.start + timedelta(hours=self.hours_difference)
        self.data['stop_real'] = self.data.stop + timedelta(hours=self.hours_difference)
        self.data['start_time_real'] = round(self.data.start_real.dt.hour + self.data.start_real.dt.minute / 60, 2)
        self.data['stop_time_real'] = round(self.data.stop_real.dt.hour + self.data.stop_real.dt.minute / 60, 2)

    def get_days_and_month_from_date(self) -> None:
        self.data['start_weekday_real'] = self.data.start_real.dt.dayofweek
        self.data['stop_weekday_real'] = self.data.stop_real.dt.dayofweek
        self.data['start_month_real'] = self.data.start_real.dt.month
        self.data['year_real'] = self.data.start_real.dt.year

    def get_days_and_month_names(self) -> None:
        self.data['start_weekday_name_real'] = self.data.start_real.dt.day_name()
        self.data['stop_weekday_name_real'] = self.data.stop_real.dt.day_name()
        self.data['start_month_name_real'] = self.data.start_real.dt.month_name()
        self.data['stop_month_name_real'] = self.data.stop_real.dt.month_name()

    def set_the_order_of_days_and_months(self) -> None:
        self.data["start_weekday_name_real"] = self.data["start_weekday_name_real"].astype('category')
        self.data["start_weekday_name_real"] = self.data["start_weekday_name_real"].cat.set_categories(
            self.day_of_the_week_names)
        self.data["stop_weekday_name_real"] = self.data["stop_weekday_name_real"].astype('category')
        self.data["stop_weekday_name_real"] = self.data["stop_weekday_name_real"].cat.set_categories(
            self.day_of_the_week_names)
        self.data["start_month_name_real"] = self.data["start_month_name_real"].astype('category')
        self.data["start_month_name_real"] = self.data["start_month_name_real"].cat.set_categories(
            self.month_names)
        self.data["stop_month_name_real"] = self.data["stop_month_name_real"].astype('category')
        self.data["stop_month_name_real"] = self.data["stop_month_name_real"].cat.set_categories(
            self.month_names)

    def write_statistics_to_csv(self) -> None:

        desired_columns = self.data.describe()[['totalSleepTime_hours', 'deepSleepTime_hours', 'shallowSleepTime_hours',
                                                'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio']]\
            .round(2)

        desired_columns.columns = ['Total sleep time (hours)', 'Deep sleep time (hours)', 'Shallow sleep time (hours)',
                                   'Start sleep time', 'Stop sleep time', 'Deep sleep time/Total sleep time ratio']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)

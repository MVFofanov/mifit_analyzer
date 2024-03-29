import pandas as pd

from abstract_classes.mifit_abstract import MiFitDataAbstract, convert_csv_to_markdown


class ActivityStageData(MiFitDataAbstract):

    def __init__(self, input_directory: str = '/mnt/c/mifit_data/mifit_analyzer/data/ACTIVITY_STAGE',
                 start_date: str | None = None, end_date: str | None = None, date_format: str = '%Y.%m.%d',
                 results_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results') -> None:

        super().__init__(input_directory, start_date, end_date, date_format,
                         results_directory)
        self.statistics_file_name = f'{self.statistics_directory}/activity_stage_statistics'

    def transform_data_for_analysis(self) -> None:
        self.transform_time_columns_to_datetime()
        self.add_new_columns()
        self.select_date_range()
        self.create_service_directories()

        self.is_prepared = True

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

        self.data['start_hour'] = self.data.start.dt.hour + self.data.start.dt.minute / 60
        self.data['stop_hour'] = self.data.stop.dt.hour + self.data.stop.dt.minute / 60

        self.data['weekday_name'] = self.data.date.dt.day_name()
        self.data["weekday_name"] = self.data["weekday_name"].astype('category')
        self.data["weekday_name"] = self.data["weekday_name"].cat.set_categories(
            self.day_of_the_week_names)

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

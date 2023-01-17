import pandas as pd

from activity.activity import ActivityData
from abstract_classes.mifit_abstract import convert_csv_to_markdown
from sleep.sleep import SleepData


class SleepActivityData(SleepData, ActivityData):
    statistics_file_name = './mifit_analyzer/statistics/sleep_activity_statistics'

    def __init__(self, sleep: SleepData, activity: ActivityData) -> None:

        self.sleep_for_merge: pd.DataFramee = \
            sleep.data[['date', 'deepSleepTime_hours',
                        'shallowSleepTime_hours', 'totalSleepTime_hours', 'start_weekday_real',
                        'stop_weekday_real', 'start_month_real', 'start_weekday_name_real',
                        'stop_weekday_name_real', 'start_month_name_real', 'stop_month_name_real',
                        'year_real', 'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio']]

        self.activity_for_merge: pd.DataFrame = activity.data[['date', 'steps', 'distance', 'runDistance', 'calories',
                                                               'date_month_name', 'date_weekday_name', 'year']]
        self.data: pd.DataFrame = pd.merge(self.sleep_for_merge, self.activity_for_merge, on='date')

        self.sleep_for_merge = None
        self.activity_for_merge = None

        self.steps_axis_labels = [i for i in range(0, self.data.steps.max(), 2000)]
        self.distance_axis_labels = [i for i in range(0, self.data.distance.max(), 2000)]

    def __repr__(self) -> str:
        return 'SleepActivityData()'

    def write_statistics_to_csv(self) -> None:
        desired_columns = self.data.describe()[['totalSleepTime_hours', 'deepSleepTime_hours', 'shallowSleepTime_hours',
                                                'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio',
                                                'steps', 'distance', 'runDistance', 'calories']]\
            .round(2)

        desired_columns.columns = ['Total sleep time (hours)', 'Deep sleep time (hours)', 'Shallow sleep time (hours)',
                                   'Start sleep time', 'Stop sleep time', 'Deep sleep time/Total sleep time ratio',
                                   'Steps', 'Distance', 'Run distance', 'Calories']

        desired_columns.to_csv(f'{self.statistics_file_name}.csv')

        convert_csv_to_markdown(csv_file=self.statistics_file_name)

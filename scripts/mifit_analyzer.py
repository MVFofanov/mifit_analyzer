from pympler import asizeof

from activity import ActivityData
from activity_stage import ActivityStageData
from report import MifitReport
from sleep import SleepData
from sleep_activity import SleepActivityData


def print_size_of_object(obj: SleepData | ActivityData | ActivityStageData | SleepActivityData | MifitReport) -> None:
    return print(f'{str(obj).split("(")[0]} object size is {asizeof.asizeof(obj) / 8 / 1024} Kb')


def main(hours_difference: int, daily_steps_goal: int = 10000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None,
         top_step_days_number: int = 10, date_format: str = '%Y.%m.%d') -> None:

    sleep = SleepData(start_date=start_date, end_date=end_date, hours_difference=hours_difference,
                      date_format=date_format)
    sleep.transform_data_for_analysis()
    sleep.write_statistics_to_csv()
    print_size_of_object(sleep)
    # print(f'Sleep object size is {asizeof.asizeof(sleep) / 8 / 1024} Kb')

    activity = ActivityData(start_date=start_date, end_date=end_date, date_format=date_format)
    activity.transform_data_for_analysis()
    activity.write_statistics_to_csv()
    print_size_of_object(activity)
    # print(f'Activity object size is {asizeof.asizeof(activity) / 8 / 1024} Kb')

    activity_stage = ActivityStageData(start_date=start_date, end_date=end_date, date_format=date_format)
    activity_stage.transform_data_for_analysis()
    activity_stage.write_statistics_to_csv()
    print_size_of_object(activity_stage)
    # print(f'Activity stage object size is {asizeof.asizeof(activity_stage) / 8 / 1024} Kb')

    sleep_activity = SleepActivityData(sleep=sleep, activity=activity)
    sleep_activity.write_statistics_to_csv()
    print_size_of_object(sleep_activity)

    report = MifitReport(mifit_data=sleep_activity,
                         activity_stage=activity_stage,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal,
                         top_step_days_number=top_step_days_number,
                         date_format=date_format)
    report.make_plots()
    report.make_report()
    print_size_of_object(report)


if __name__ == "__main__":
    main(user_name='Mikhail',
         hours_difference=7,
         daily_steps_goal=8000,
         start_date='1900.07.02',
         end_date='2077.05.04')

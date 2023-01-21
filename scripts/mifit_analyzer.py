from pympler import asizeof
from typing import Any

from abstract_classes.mifit_data import MiFitData
from activity.activity import ActivityData
from activity_stage.activity_stage import ActivityStageData
from report.report import MifitReport
from sleep.sleep import SleepData
from sleep_activity.sleep_activity import SleepActivityData


def print_size_of_object(obj: Any) -> None:
    return print(f'{str(obj).split("(")[0]} object size is {round(asizeof.asizeof(obj) / 1024 / 1024, 2)} Mb')


def main(hours_difference: int, daily_steps_goal: int = 8000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None,
         top_step_days_number: int = 10, date_format: str = '%Y.%m.%d') -> None:

    sleep = SleepData(start_date=start_date, end_date=end_date, hours_difference=hours_difference,
                      date_format=date_format)
    sleep.transform_data_for_analysis()
    sleep.write_statistics_to_csv()
    print_size_of_object(sleep)
    # print(type(sleep))

    activity = ActivityData(start_date=start_date, end_date=end_date, date_format=date_format)
    activity.transform_data_for_analysis()
    activity.write_statistics_to_csv()
    print_size_of_object(activity)

    activity_stage = ActivityStageData(start_date=start_date, end_date=end_date, date_format=date_format)
    activity_stage.transform_data_for_analysis()
    activity_stage.write_statistics_to_csv()
    print_size_of_object(activity_stage)

    sleep_activity = SleepActivityData(sleep=sleep, activity=activity)
    sleep_activity.write_statistics_to_csv()
    print_size_of_object(sleep_activity)

    mifit_data = MiFitData(sleep=sleep, activity=activity, sleep_activity=sleep_activity,
                           activity_stage=activity_stage)

    report = MifitReport(mifit_data=mifit_data,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal,
                         top_step_days_number=top_step_days_number,
                         date_format=date_format)
    report.make_plots()
    report.make_report()
    print_size_of_object(report)
    # print(type(report))


if __name__ == "__main__":
    main(user_name='User_name',
         start_date='2019.03.15',
         end_date='2023.06.13',
         hours_difference=7
         )

from activity import Activity
from mifit_report import MifitReport
from sleep import Sleep
from sleep_activity import SleepActivity


def main(hours_difference: int, daily_steps_goal: int = 10000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None,
         top_step_days_number: int = 10, date_format: str = '%Y.%m.%d') -> None:

    sleep1 = Sleep(start_date=start_date, end_date=end_date, hours_difference=hours_difference,
                   date_format=date_format)
    sleep1.transform_data_for_analysis()
    sleep1.write_statistics_to_csv()

    activity1 = Activity(start_date=start_date, end_date=end_date, date_format=date_format)
    activity1.transform_data_for_analysis()
    activity1.write_statistics_to_csv()

    mifit_data = SleepActivity(sleep=sleep1, activity=activity1)
    mifit_data.write_statistics_to_csv()

    report = MifitReport(mifit_data=mifit_data,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal,
                         top_step_days_number=top_step_days_number,
                         date_format=date_format)
    report.make_plots()
    report.make_report()


if __name__ == "__main__":
    main(user_name='Mikhail',
         hours_difference=7,
         daily_steps_goal=8000,
         start_date='1900.07.02',
         end_date='2077.05.04')

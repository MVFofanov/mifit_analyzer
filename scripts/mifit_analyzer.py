from activity import Activity
from mifit_report import MifitReport
from sleep import Sleep
from sleep_activity import SleepActivity


def main(hours_difference: int, daily_steps_goal: int = 10000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None) -> None:

    sleep1 = Sleep(start_date=start_date, end_date=end_date, hours_difference=hours_difference)
    sleep1.transform_data_for_analysis()
    sleep1.write_statistics_to_csv()

    activity1 = Activity(start_date=start_date, end_date=end_date)
    activity1.transform_data_for_analysis()
    activity1.write_statistics_to_csv()

    mifit_data = SleepActivity(sleep1, activity1)
    mifit_data.write_statistics_to_csv()

    report = MifitReport(mifit_data=mifit_data,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal)
    report.make_plots()
    report.make_report()


if __name__ == "__main__":
    main(user_name='Mikhail',
         hours_difference=7,
         daily_steps_goal=8000,
         start_date=None,
         end_date=None)

import logging
from pathlib import Path
from time import perf_counter

from mifit_dataclasses.mifit_data import MiFitData
from activity.activity import ActivityData
from activity_stage.activity_stage import ActivityStageData
from report.report import MifitReport
from sleep.sleep import SleepData
from sleep_activity.sleep_activity import SleepActivityData


def main(hours_difference: int = 0, daily_steps_goal: int = 8000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None,
         top_step_days_number: int = 10, date_format: str = '%Y.%m.%d',
         output_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results', log_mode: str = 'w') -> None:
    start_time = perf_counter()

    log_directory = f'{output_directory}/logs'
    log_file_name = f'{log_directory}/logs.log'
    log_format = '%(levelname)s\t%(asctime)s\t%(module)s\t%(funcName)s\t%(message)s'
    lof_level = logging.INFO

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    Path(log_directory).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(filename=log_file_name, filemode=log_mode, format=log_format,
                        level=lof_level, encoding='utf-8')

    logging.info('Mifit_analyzer has started its work')

    sleep = SleepData(start_date=start_date, end_date=end_date,
                      date_format=date_format, hours_difference=hours_difference,
                      results_directory=output_directory)
    sleep.transform_data_for_analysis()
    sleep.write_statistics_to_csv()

    logging.info(f"Sleep object have been analyzed. {sleep.get_size()}")

    activity = ActivityData(start_date=start_date, end_date=end_date, date_format=date_format,
                            results_directory=output_directory)
    activity.transform_data_for_analysis()
    activity.write_statistics_to_csv()

    logging.info(f"Activity object have been analyzed. {activity.get_size()}")

    activity_stage = ActivityStageData(start_date=start_date, end_date=end_date, date_format=date_format,
                                       results_directory=output_directory)
    activity_stage.transform_data_for_analysis()
    activity_stage.write_statistics_to_csv()

    logging.info(f"Activity_stage object have been analyzed. {activity_stage.get_size()}")

    sleep_activity = SleepActivityData(sleep=sleep, activity=activity, results_directory=output_directory)
    sleep_activity.write_statistics_to_csv()

    logging.info(f"Sleep_activity object have been analyzed. {sleep_activity.get_size()}")

    mifit_data = MiFitData(sleep=sleep, activity=activity, sleep_activity=sleep_activity,
                           activity_stage=activity_stage)

    report = MifitReport(mifit_data=mifit_data,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal,
                         top_step_days_number=top_step_days_number,
                         date_format=date_format,
                         results_directory=output_directory)

    logging.info(f"Report object have been analyzed. {report.get_size()}")

    report.make_plots()

    logging.info("Report plots were built")

    report.make_report()

    logging.info("Report has been successfully generated")

    logging.info("Mifit_analyzer has finished its work")

    end_time = perf_counter()
    elapsed_time = end_time - start_time

    logging.info(f"Program execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main(user_name='User_name',
         start_date='2019.03.15',
         end_date='2023.06.13',
         hours_difference=7,
         output_directory='/mnt/c/mifit_data/mifit_analyzer/super_results'
         )

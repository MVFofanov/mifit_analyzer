import argparse
import logging
from pathlib import Path
import sys
from time import perf_counter

from mifit_dataclasses.mifit_data import MiFitData
from activity.activity import ActivityData
from activity_stage.activity_stage import ActivityStageData
from report.report import MifitReport
from sleep.sleep import SleepData
from sleep_activity.sleep_activity import SleepActivityData


def parse_arguments():
    parser = argparse.ArgumentParser(prog='mifit_analyzer', usage='python3 %(prog)s [options]',
                                     description='This tool analyzes the data (steps and sleep) received from '
                                                 'the Mi Band fitness bracelet and generates a report based on it.')
    parser.add_argument('--input_directory', help='path to input directory. Default: mifit_analyzer/data', type=str,
                        default='/mnt/c/mifit_data/mifit_analyzer/data')
    parser.add_argument('--start_date', help='start date. Default: 1900.01.01', type=str, default='1900.01.01')
    parser.add_argument('--end_date', help='end date. Default: 2100.01.01', type=str, default='2100.01.01')
    parser.add_argument('--time_zone', help='time zone. Default: 0', type=int, default=0)
    parser.add_argument('--output_directory', help='path to output directory. '
                                                   'Default: mifit_analyzer/results', type=str,
                        default='/mnt/c/mifit_data/mifit_analyzer/results')
    parser.add_argument('--daily_steps_goal', help='daily steps goal. Default: 8000', type=int, default=8000)
    parser.add_argument('--user_name', help='user name. Default: Username', type=str, default='Username')
    parser.add_argument('--top_step_days_number', help='top step days number. Default: 10', type=int, default=10)
    parser.add_argument('--date_format', help='date format. Default: YYYY.mm.dd', type=str, default='%Y.%m.%d')
    parser.add_argument('--log_mode', help='log mode. Default: w', type=str, default='w')
    args = parser.parse_args()
    return args


def main(input_directory: str = '/mnt/c/mifit_data/mifit_analyzer/data',
         hours_difference: int = 0, daily_steps_goal: int = 8000, user_name: str = 'Username',
         start_date: str | None = None, end_date: str | None = None,
         top_step_days_number: int = 10, date_format: str = '%Y.%m.%d',
         output_directory: str = '/mnt/c/mifit_data/mifit_analyzer/results') -> None:

    input_directory = input_directory.removesuffix('/')
    output_directory = output_directory.removesuffix('/')

    sleep = SleepData(input_directory=f'{input_directory}/SLEEP',
                      start_date=start_date, end_date=end_date,
                      date_format=date_format, hours_difference=hours_difference,
                      results_directory=output_directory)
    sleep.transform_data_for_analysis()
    sleep.write_statistics_to_csv()

    sleep.make_logging_message()

    activity = ActivityData(input_directory=f'{input_directory}/ACTIVITY',
                            start_date=start_date, end_date=end_date, date_format=date_format,
                            results_directory=output_directory)
    activity.transform_data_for_analysis()
    activity.write_statistics_to_csv()

    activity.make_logging_message()

    activity_stage = ActivityStageData(input_directory=f'{input_directory}/ACTIVITY_STAGE',
                                       start_date=start_date, end_date=end_date, date_format=date_format,
                                       results_directory=output_directory)
    activity_stage.transform_data_for_analysis()
    activity_stage.write_statistics_to_csv()

    activity_stage.make_logging_message()

    sleep_activity = SleepActivityData(sleep=sleep, activity=activity, results_directory=output_directory)
    sleep_activity.write_statistics_to_csv()

    sleep_activity.make_logging_message()

    mifit_data = MiFitData(sleep=sleep, activity=activity, sleep_activity=sleep_activity,
                           activity_stage=activity_stage)

    report = MifitReport(mifit_data=mifit_data,
                         user_name=user_name,
                         daily_steps_goal=daily_steps_goal,
                         top_step_days_number=top_step_days_number,
                         date_format=date_format,
                         results_directory=output_directory)

    report.make_logging_message()

    report.make_plots()

    logging.info("Report plots were built")

    report.make_report()

    logging.info("Report has been successfully generated")


if __name__ == "__main__":
    args = parse_arguments()

    start_time = perf_counter()

    log_directory = f'{args.output_directory}/logs'
    log_file_name = f'{log_directory}/logs.log'
    log_format = '%(levelname)s\t%(asctime)s\t%(module)s\t%(funcName)s\t%(message)s'
    log_level = logging.INFO

    Path(args.output_directory).mkdir(parents=True, exist_ok=True)
    Path(log_directory).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(filename=log_file_name, filemode=args.log_mode, format=log_format,
                        level=log_level, encoding='utf-8')

    logging.info('Mifit_analyzer has started its work')
    logging.info('To reproduce this analysis, you can use the following command:')
    logging.info(f'python3 {" ".join(sys.argv)}')

    logging.info(f"main(input_directory='{args.input_directory}', "
                 f"user_name='{args.user_name}', "
                 f"start_date='{args.start_date}', "
                 f"end_date='{args.end_date}', "
                 f"hours_difference={args.time_zone}, "
                 f"output_directory='{args.output_directory}', "
                 f"daily_steps_goal={args.daily_steps_goal}, "
                 f"top_step_days_number={args.top_step_days_number}, "
                 f"date_format='{args.date_format}')"
                 )

    main(input_directory=args.input_directory,
         user_name=args.user_name,
         start_date=args.start_date,
         end_date=args.end_date,
         hours_difference=args.time_zone,
         output_directory=args.output_directory,
         daily_steps_goal=args.daily_steps_goal,
         top_step_days_number=args.top_step_days_number,
         date_format=args.date_format
         )

    logging.info("Mifit_analyzer has finished its work")

    end_time = perf_counter()
    elapsed_time = end_time - start_time

    logging.info(f"Program execution time: {elapsed_time:.2f} seconds")

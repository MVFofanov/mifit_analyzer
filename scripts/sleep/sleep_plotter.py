from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from abstract_classes.plotter_abstract import PlotterAbstract


class SleepPlotter(PlotterAbstract):

    def make_sleep_hours_pairplot(self) -> None:
        sleep_hours = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']]

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.pairplot(sleep_hours)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_pairplot.png'))
        plt.close("all")

    def make_sleep_hours_boxplot(self) -> None:
        sleep_hours = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']]
        fig, axs = plt.subplots(ncols=3, nrows=1, figsize=self.plot_figsize)
        index = 0
        axs = axs.flatten()
        for k, v in sleep_hours.items():
            sns.boxplot(y=k, data=sleep_hours, ax=axs[index])
            index += 1
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)
        plt.close("all")

    def make_sleep_hours_correlations_plot(self) -> None:
        correlations = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours']].corr()
        correlations = correlations * 100

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.heatmap(correlations, annot=True, fmt='.0f')

        plt.title('Sleep time correlations plot', fontsize=self.title_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_correlations_plot.png'))
        plt.close("all")

    def make_sleep_correlations_plot(self) -> None:
        columns = self.data[['deepSleepTime_hours', 'shallowSleepTime_hours', 'totalSleepTime_hours',
                             'start_weekday_real', 'stop_weekday_real', 'start_month_real', 'year_real',
                             'start_time_real', 'stop_time_real', 'deep_total_sleep_ratio']]

        correlations = columns.corr()
        correlations = correlations * 100

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.heatmap(correlations, annot=True, fmt='.0f')

        plt.title('Sleep time correlations plot', fontsize=self.title_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_correlations_plot.png'))
        plt.close("all")

    def make_sleep_hours_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="shallowSleepTime_hours", y="deepSleepTime_hours",
                        hue="start_weekday_name_real")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow and deep sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Shallow sleep, hours", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep, hours", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'sleep_hours_scatterplot.png'))
        plt.close("all")

    def make_sleep_hours_per_start_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per day of the week when fall asleep plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_per_start_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_stop_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="stop_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per day of the week when woke up plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_per_stop_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_start_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_per_start_month_boxplot.png'))
        plt.close("all")

    def make_sleep_start_and_stop_time_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="start_time_real", y="stop_time_real", hue="start_weekday_name_real")

        plt.xticks(self.hour_axis_labels)
        plt.yticks(self.hour_axis_labels)
        plt.title('Start and stop sleep time plot', fontsize=self.title_fontsize)
        plt.xlabel("Start sleep time", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'sleep_start_and_stop_time_scatterplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_start_time_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="stop_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_stop_time_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_start_time_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="stop_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_stop_time_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_start_time_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="start_time_real", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Start sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Start sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_start_time_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_stop_time_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="stop_time_real", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Stop sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Stop sleep time", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_stop_time_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_deep_hours_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="start_weekday_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_shallow_hours_per_weekday_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_deep_hours_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="start_month_name_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_shallow_hours_per_month_boxplot.png'))
        plt.close("all")

    def make_sleep_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="totalSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Total sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Total sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_hours_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_deep_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="deepSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Deep sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Deep sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_deep_hours_per_year_boxplot.png'))
        plt.close("all")

    def make_sleep_shallow_hours_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="shallowSleepTime_hours", x="year_real")

        plt.yticks(self.hour_axis_labels)
        plt.title('Shallow sleep time per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Shallow sleep time, hours", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'sleep_shallow_hours_per_year_boxplot.png'))
        plt.close("all")

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from abstract_classes.plotter_abstract import ActivityPlotterAbstract


class ActivityPlotter(ActivityPlotterAbstract):

    def make_activity_pairplot(self) -> None:
        activity_data = self.data[['steps', 'distance', 'runDistance', 'calories']]

        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.pairplot(activity_data)

        plt.savefig(Path(self.plots_directory, 'activity_pairplot.png'))
        plt.close("all")

    def make_activity_boxplot(self) -> None:
        activity_data = self.data[['steps', 'distance', 'runDistance', 'calories']]
        fig, axs = plt.subplots(ncols=4, nrows=1, figsize=(10, 5))
        index = 0
        axs = axs.flatten()
        for k, v in activity_data.items():
            sns.boxplot(y=k, data=activity_data, ax=axs[index])
            index += 1
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)

        plt.savefig(Path(self.plots_directory, 'activity_boxplot.png'))
        plt.close("all")

    def make_activity_steps_distance_scatterplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.scatterplot(data=self.data, x="steps", y="distance", hue="date_weekday_name")

        plt.xticks(self.steps_axis_labels)
        plt.yticks(self.distance_axis_labels)
        plt.title('Steps and distance plot', fontsize=self.title_fontsize)
        plt.xlabel("Steps", fontsize=self.label_fontsize)
        plt.ylabel("Distance", fontsize=self.label_fontsize)
        plt.legend(title="Day of the week")

        plt.savefig(Path(self.plots_directory, 'activity_steps_distance_scatterplot.png'))
        plt.close("all")

    def make_activity_steps_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="date_weekday_name")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_weekday_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_weekday_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="date_weekday_name")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per day of the week plot', fontsize=self.title_fontsize)
        plt.xlabel("Day of the week", fontsize=self.label_fontsize)
        plt.ylabel("Distance", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_weekday_boxplot.png'))
        plt.close("all")

    def make_activity_steps_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="date_month_name")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_month_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_month_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="date_month_name")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per month plot', fontsize=self.title_fontsize)
        plt.xlabel("Month", fontsize=self.label_fontsize)
        plt.ylabel("Distance, m", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_month_boxplot.png'))
        plt.close("all")

    def make_activity_steps_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="steps", x="year")

        plt.yticks(self.steps_axis_labels)
        plt.title('Steps per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Steps", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_steps_per_year_boxplot.png'))
        plt.close("all")

    def make_activity_distance_per_year_boxplot(self) -> None:
        sns.set_style('whitegrid')
        plt.figure(figsize=self.plot_figsize)

        sns.boxplot(data=self.data, y="distance", x="year")

        plt.yticks(self.distance_axis_labels)
        plt.title('Distance per year plot', fontsize=self.title_fontsize)
        plt.xlabel("Year", fontsize=self.label_fontsize)
        plt.ylabel("Distance, m", fontsize=self.label_fontsize)

        plt.savefig(Path(self.plots_directory, 'activity_distance_per_year_boxplot.png'))
        plt.close("all")

from sleep.sleep_plotter import SleepPlotter


class SleepReportPlotter:
    plots_directory = './mifit_analyzer/plots/'

    hour_axis_labels = [i for i in range(0, 25, 2)]
    title_fontsize = 20
    label_fontsize = 16
    plot_figsize = (12, 8)

    def __init__(self, plotter: SleepPlotter, markdown_plots_list: list[str]):
        self.plotter = plotter
        self.markdown_plots_list = markdown_plots_list

    def get_plot_markdown_text(self, file_name: str) -> tuple[str, str]:
        plot_path = f'{self.plots_directory}/{file_name}.png'
        plot_name = f"{plot_path.split('/')[-1]}"
        plot_markdown = f"![image]({plot_path})"
        return plot_name, plot_markdown

    def make_sleep_plots(self) -> None:
        self._make_sleep_common_plots()
        self._make_sleep_hours_boxplots()
        self._make_sleep_deep_and_shallow_hours_boxplots()
        self._make_sleep_start_and_stop_time_plots()

    def _make_sleep_common_plots(self) -> None:
        self.plotter.make_sleep_hours_pairplot()
        self.plotter.make_sleep_hours_boxplot()
        self.plotter.make_sleep_hours_correlations_plot()
        self.plotter.make_sleep_correlations_plot()
        self.plotter.make_sleep_hours_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep common plots\n',
                                         *self.get_plot_markdown_text('sleep_hours_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_correlations_plot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_correlations_plot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_scatterplot'))

    def _make_sleep_start_and_stop_time_plots(self) -> None:
        self.plotter.make_sleep_start_and_stop_time_scatterplot()

        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_and_stop_time_scatterplot'))

        self._make_sleep_start_time_boxplots()
        self._make_sleep_stop_time_boxplots()

    def _make_sleep_start_time_boxplots(self) -> None:
        self.plotter.make_sleep_start_time_per_weekday_boxplot()
        self.plotter.make_sleep_start_time_per_month_boxplot()
        self.plotter.make_sleep_start_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep start time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_start_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_start_time_per_year_boxplot'))

    def _make_sleep_stop_time_boxplots(self) -> None:
        self.plotter.make_sleep_stop_time_per_weekday_boxplot()
        self.plotter.make_sleep_stop_time_per_month_boxplot()
        self.plotter.make_sleep_stop_time_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep stop time boxplots\n',
                                         *self.get_plot_markdown_text('sleep_stop_time_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_hours_boxplots(self) -> None:
        self.plotter.make_sleep_hours_per_start_weekday_boxplot()
        self.plotter.make_sleep_hours_per_stop_weekday_boxplot()

        self.plotter.make_sleep_hours_per_start_month_boxplot()
        self.plotter.make_sleep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_hours_per_start_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_stop_weekday_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_hours_per_start_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_stop_time_per_year_boxplot'))

    def _make_sleep_deep_and_shallow_hours_boxplots(self) -> None:
        self._make_sleep_deep_hours_boxplots()
        self._make_sleep_shallow_hours_boxplots()

        # self.markdown_plots_list.extend(('Here you can find your deep and shallow sleep hours_boxplots\n',
        #                                  *self.get_plot_markdown_text('sleep_deep_hours_boxplots')))
        # self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_boxplots'))

    def _make_sleep_deep_hours_boxplots(self) -> None:
        self.plotter.make_sleep_deep_hours_per_weekday_boxplot()
        self.plotter.make_sleep_deep_hours_per_month_boxplot()
        self.plotter.make_sleep_deep_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep deep hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_deep_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_deep_hours_per_year_boxplot'))

    def _make_sleep_shallow_hours_boxplots(self) -> None:
        self.plotter.make_sleep_shallow_hours_per_weekday_boxplot()
        self.plotter.make_sleep_shallow_hours_per_month_boxplot()
        self.plotter.make_sleep_shallow_hours_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your sleep shallow hours boxplots\n',
                                         *self.get_plot_markdown_text('sleep_shallow_hours_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_shallow_hours_per_year_boxplot'))

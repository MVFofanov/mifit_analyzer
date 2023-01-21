from abstract_classes.report_plotter_abstract import ReportPlotterAbstract, markdown_text
from sleep_activity.sleep_activity_plotter import SleepActivityPlotter


class SleepActivityReportPlotter(ReportPlotterAbstract):

    def __init__(self, plotter: SleepActivityPlotter, markdown_plots_list: list[markdown_text]):
        self.plotter = plotter
        super().__init__(self.plotter, markdown_plots_list)

    def make_plots(self) -> None:
        self.plotter.make_sleep_activity_correlations_plot()
        self.plotter.make_sleep_activity_steps_sleep_per_start_weekday_scatterplot()
        self.plotter.make_sleep_activity_steps_sleep_per_stop_weekday_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your sleep activity plots\n',
                                         *self.get_plot_markdown_text('sleep_activity_correlations_plot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_start_weekday'
                                                                    '_scatterplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('sleep_activity_steps_sleep_per_stop_weekday'
                                                                    '_scatterplot'))

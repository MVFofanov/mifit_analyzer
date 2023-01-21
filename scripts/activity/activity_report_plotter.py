from abstract_classes.report_plotter_abstract import ReportPlotterAbstract, markdown_text
from activity.activity_plotter import ActivityPlotter


class ActivityReportPlotter(ReportPlotterAbstract):

    def __init__(self, plotter: ActivityPlotter, markdown_plots_list: list[markdown_text]):
        self.plotter = plotter
        super().__init__(self.plotter, markdown_plots_list)

    def make_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your activity plots\n')

        self._make_activity_distance_common_plots()

        self._make_activity_distance_boxplots()

        self._make_activity_steps_boxplots()

    def _make_activity_distance_common_plots(self) -> None:
        self.plotter.make_activity_pairplot()
        self.plotter.make_activity_boxplot()
        self.plotter.make_activity_steps_distance_scatterplot()

        self.markdown_plots_list.extend(('Here you can find your common activity plots\n',
                                         *self.get_plot_markdown_text('activity_pairplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_distance_scatterplot'))

    def _make_activity_distance_boxplots(self) -> None:
        self.plotter.make_activity_distance_per_weekday_boxplot()
        self.plotter.make_activity_distance_per_month_boxplot()
        self.plotter.make_activity_distance_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity distance boxplots\n',
                                         *self.get_plot_markdown_text('activity_distance_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_distance_per_year_boxplot'))

    def _make_activity_steps_boxplots(self) -> None:
        self.plotter.make_activity_steps_per_weekday_boxplot()
        self.plotter.make_activity_steps_per_month_boxplot()
        self.plotter.make_activity_steps_per_year_boxplot()

        self.markdown_plots_list.extend(('Here you can find your activity steps boxplots\n',
                                         *self.get_plot_markdown_text('activity_steps_per_weekday_boxplot')))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_month_boxplot'))
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_steps_per_year_boxplot'))

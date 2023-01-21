from abstract_classes.report_plotter_abstract import ReportPlotterAbstract, markdown_text
from activity_stage.activity_stage_plotter import ActivityStagePlotter


class ActivityStageReportPlotter(ReportPlotterAbstract):

    def __init__(self, plotter: ActivityStagePlotter, markdown_plots_list: list[markdown_text]):
        self.plotter = plotter
        super().__init__(self.plotter, markdown_plots_list)

    def make_plots(self) -> None:
        self.markdown_plots_list.append('Here you can find your activity stage plots\n')

        self._make_activity_stage_km_h_plots()
        self._make_activity_stage_scatterplots()

    def _make_activity_stage_km_h_plots(self) -> None:
        self.plotter.make_activity_stage_histplot_km_h()
        self.markdown_plots_list.extend(self.get_plot_markdown_text('activity_stage_histplot_km_h'))

    def _make_activity_stage_scatterplots(self) -> None:
        self.plotter.make_activity_stage_start_stop_hour_per_weekday_scatterplot()
        self.markdown_plots_list.extend(self.get_plot_markdown_text(
            'activity_stage_start_stop_hour_per_weekday_scatterplot'))

        self.plotter.make_activity_stage_start_hour_and_steps_per_weekday_scatterplot()
        self.markdown_plots_list.extend(self.get_plot_markdown_text(
            'activity_stage_start_hour_and_steps_per_weekday_scatterplot'))
